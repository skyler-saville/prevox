"""Minimal Standard MIDI File export for Music IR.

This renderer intentionally owns the temporary 12-TET preview mapping, velocity,
channel, and ticks-per-beat choices. Those concepts must not leak into Music IR.
"""

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import BinaryIO, Iterable, Mapping

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

from prevox.domain import MusicIR, Pitch, RealizedNote

_PITCH_CLASS_TO_SEMITONE = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
}

GM_DRUM_CHANNEL = 9
GM_DRUM_NOTES = {
    "kick": 36,
    "snare": 38,
    "closed_hat": 42,
    "open_hat": 46,
    "crash": 49,
    "ride": 51,
}


def midi_note_number(pitch: Pitch) -> int:
    """Map a spelled Pitch to a MIDI note number using preview 12-TET policy."""
    if not isinstance(pitch, Pitch):
        raise TypeError("pitch must be a Pitch")
    semitone = (
        _PITCH_CLASS_TO_SEMITONE[pitch.pitch_class.step]
        + pitch.pitch_class.accidental
    )
    note_number = (pitch.octave + 1) * 12 + semitone
    if not 0 <= note_number <= 127:
        raise ValueError(f"pitch {pitch} is outside MIDI note range 0..127")
    return note_number


def _ticks(value: Fraction, *, ticks_per_beat: int, field: str) -> int:
    raw_ticks = value * ticks_per_beat
    if raw_ticks.denominator != 1:
        raise ValueError(
            f"{field} {value} is not representable with "
            f"{ticks_per_beat} ticks per beat"
        )
    return raw_ticks.numerator


def _validate_channel(channel: int) -> None:
    if (
        isinstance(channel, bool)
        or not isinstance(channel, int)
        or not 0 <= channel <= 15
    ):
        raise ValueError("channel must be between 0 and 15")


def _validate_velocity(velocity: int) -> None:
    if (
        isinstance(velocity, bool)
        or not isinstance(velocity, int)
        or not 1 <= velocity <= 127
    ):
        raise ValueError("velocity must be between 1 and 127")


def _validate_program(program: int) -> None:
    if (
        isinstance(program, bool)
        or not isinstance(program, int)
        or not 0 <= program <= 127
    ):
        raise ValueError("program must be between 0 and 127")


def _validate_drum_note(note: int) -> None:
    if isinstance(note, bool) or not isinstance(note, int) or not 0 <= note <= 127:
        raise ValueError("drum MIDI note must be between 0 and 127")


def _default_preview_drum_map() -> dict[Pitch, int]:
    return {
        Pitch.parse("C2"): GM_DRUM_NOTES["kick"],
        Pitch.parse("D2"): GM_DRUM_NOTES["snare"],
        Pitch.parse("F#2"): GM_DRUM_NOTES["closed_hat"],
        Pitch.parse("G#2"): GM_DRUM_NOTES["open_hat"],
        Pitch.parse("C#3"): GM_DRUM_NOTES["crash"],
        Pitch.parse("D#3"): GM_DRUM_NOTES["ride"],
    }


@dataclass(frozen=True, slots=True)
class MidiVoiceAssignment:
    """Renderer-local MIDI preview choices for one logical voice."""

    channel: int
    program: int | None = None
    velocity: int | None = None
    track_name: str | None = None
    drum_map: tuple[tuple[Pitch, int], ...] = ()

    def __post_init__(self) -> None:
        _validate_channel(self.channel)
        if self.program is not None:
            _validate_program(self.program)
        if self.velocity is not None:
            _validate_velocity(self.velocity)
        if self.track_name is not None and not self.track_name.strip():
            raise ValueError("track_name must be non-empty when provided")
        if any(
            not isinstance(pitch, Pitch) or not isinstance(note, int)
            for pitch, note in self.drum_map
        ):
            raise TypeError("drum_map must contain Pitch to MIDI note pairs")
        seen: set[Pitch] = set()
        for pitch, note in self.drum_map:
            if pitch in seen:
                raise ValueError(f"duplicate drum_map pitch {pitch}")
            _validate_drum_note(note)
            seen.add(pitch)
        if self.drum_map and self.channel != GM_DRUM_CHANNEL:
            raise ValueError("drum_map assignments must use GM drum channel 9")

    @classmethod
    def gm_drums(
        cls,
        *,
        velocity: int | None = None,
        track_name: str = "Drums",
        drum_map: Mapping[Pitch, int] | Iterable[tuple[Pitch, int]] | None = None,
    ) -> "MidiVoiceAssignment":
        """Create a General MIDI drum assignment for a temporary preview voice."""
        selected_map = _default_preview_drum_map() if drum_map is None else drum_map
        normalized = (
            tuple(selected_map.items())
            if isinstance(selected_map, Mapping)
            else tuple(selected_map)
        )
        return cls(
            channel=GM_DRUM_CHANNEL,
            velocity=velocity,
            track_name=track_name,
            drum_map=normalized,
        )

    def note_number_for(self, pitch: Pitch) -> int:
        """Return the backend MIDI note number for a symbolic pitch."""
        for mapped_pitch, note_number in self.drum_map:
            if mapped_pitch == pitch:
                return note_number
        if self.drum_map:
            raise ValueError(f"pitch {pitch} is not present in drum_map")
        return midi_note_number(pitch)


@dataclass(frozen=True, slots=True)
class MidiRenderProfile:
    """Backend-only mapping from logical voices to MIDI preview assignments."""

    voice_assignments: tuple[tuple[str, MidiVoiceAssignment], ...]

    def __init__(
        self,
        voice_assignments: Mapping[str, MidiVoiceAssignment]
        | Iterable[tuple[str, MidiVoiceAssignment]],
    ) -> None:
        normalized = tuple(voice_assignments.items()) if isinstance(
            voice_assignments,
            Mapping,
        ) else tuple(voice_assignments)
        if not normalized:
            raise ValueError("voice_assignments must not be empty")

        seen: set[str] = set()
        for voice_id, assignment in normalized:
            if not isinstance(voice_id, str) or not voice_id.strip():
                raise ValueError("voice assignment keys must be non-empty voice ids")
            if voice_id in seen:
                raise ValueError(f"duplicate voice assignment for {voice_id!r}")
            if not isinstance(assignment, MidiVoiceAssignment):
                raise TypeError("voice assignment values must be MidiVoiceAssignment")
            seen.add(voice_id)

        object.__setattr__(self, "voice_assignments", normalized)

    def assignment_for(self, voice_id: str) -> MidiVoiceAssignment | None:
        """Return the explicit assignment for a logical voice, if present."""
        for assigned_voice_id, assignment in self.voice_assignments:
            if assigned_voice_id == voice_id:
                return assignment
        return None


@dataclass(frozen=True, slots=True)
class MidiRenderer:
    """Write Music IR to a deterministic Standard MIDI File."""

    ticks_per_beat: int = 480
    preview_velocity: int = 64
    channel: int = 0
    profile: MidiRenderProfile | None = None

    def __post_init__(self) -> None:
        if (
            isinstance(self.ticks_per_beat, bool)
            or not isinstance(self.ticks_per_beat, int)
            or self.ticks_per_beat <= 0
        ):
            raise ValueError("ticks_per_beat must be a positive integer")
        try:
            _validate_velocity(self.preview_velocity)
        except ValueError as error:
            raise ValueError("preview_velocity must be between 1 and 127") from error
        try:
            _validate_channel(self.channel)
        except ValueError as error:
            raise ValueError("channel must be between 0 and 15") from error
        if self.profile is not None and not isinstance(self.profile, MidiRenderProfile):
            raise TypeError("profile must be a MidiRenderProfile")

    def to_midi_file(self, music: MusicIR) -> MidiFile:
        """Return an in-memory Standard MIDI File for one Music IR value."""
        if not isinstance(music, MusicIR):
            raise TypeError("music must be a MusicIR")
        if self.profile is not None:
            return self._to_profiled_midi_file(music)
        return self._to_single_track_midi_file(music)

    def write(self, music: MusicIR, path: str | Path | BinaryIO) -> None:
        """Write Music IR to a Standard MIDI File path or binary file."""
        if isinstance(path, (str, Path)):
            target = Path(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            self.to_midi_file(music).save(target)
            return
        self.to_midi_file(music).save(file=path)

    def _to_single_track_midi_file(self, music: MusicIR) -> MidiFile:
        midi = MidiFile(ticks_per_beat=self.ticks_per_beat, type=1)
        track = MidiTrack()
        midi.tracks.append(track)
        track.append(MetaMessage("track_name", name=music.song.title, time=0))
        track.append(
            MetaMessage(
                "set_tempo",
                tempo=bpm2tempo(music.song.tempo_bpm),
                time=0,
            )
        )

        self._append_messages(
            track,
            self._messages(
                music.iter_notes(),
                assignment=None,
                channel=self.channel,
                velocity=self.preview_velocity,
            ),
        )
        track.append(MetaMessage("end_of_track", time=0))
        return midi

    def _to_profiled_midi_file(self, music: MusicIR) -> MidiFile:
        if self.profile is None:
            raise AssertionError("profiled MIDI export requires a profile")

        midi = MidiFile(ticks_per_beat=self.ticks_per_beat, type=1)
        conductor_track = MidiTrack()
        midi.tracks.append(conductor_track)
        conductor_track.append(
            MetaMessage("track_name", name=f"{music.song.title} Tempo", time=0)
        )
        conductor_track.append(
            MetaMessage(
                "set_tempo",
                tempo=bpm2tempo(music.song.tempo_bpm),
                time=0,
            )
        )
        conductor_track.append(MetaMessage("end_of_track", time=0))

        grouped_notes = self._notes_by_voice(music)
        for voice_id, notes in grouped_notes:
            assignment = self.profile.assignment_for(voice_id)
            if assignment is None:
                assignment = MidiVoiceAssignment(
                    channel=self.channel,
                    velocity=self.preview_velocity,
                    track_name=voice_id,
                )
            velocity = (
                assignment.velocity
                if assignment.velocity is not None
                else self.preview_velocity
            )
            track = MidiTrack()
            midi.tracks.append(track)
            track.append(
                MetaMessage(
                    "track_name",
                    name=assignment.track_name or voice_id,
                    time=0,
                )
            )
            if assignment.program is not None:
                track.append(
                    Message(
                        "program_change",
                        program=assignment.program,
                        channel=assignment.channel,
                        time=0,
                    )
                )
            self._append_messages(
                track,
                self._messages(
                    notes,
                    assignment=assignment,
                    channel=assignment.channel,
                    velocity=velocity,
                ),
            )
            track.append(MetaMessage("end_of_track", time=0))

        return midi

    def _notes_by_voice(
        self,
        music: MusicIR,
    ) -> tuple[tuple[str, tuple[RealizedNote, ...]], ...]:
        grouped: dict[str, list[RealizedNote]] = {}
        for note in music.iter_notes():
            grouped.setdefault(note.voice_id, []).append(note)
        return tuple((voice_id, tuple(notes)) for voice_id, notes in grouped.items())

    def _append_messages(
        self,
        track: MidiTrack,
        messages: tuple[tuple[int, Message], ...],
    ) -> None:
        last_tick = 0
        for tick, message in messages:
            message.time = tick - last_tick
            track.append(message)
            last_tick = tick

    def _messages(
        self,
        notes: Iterable[RealizedNote],
        *,
        assignment: MidiVoiceAssignment | None,
        channel: int,
        velocity: int,
    ) -> tuple[tuple[int, Message], ...]:
        events: list[tuple[int, int, int, Message]] = []
        for note in notes:
            note_number = (
                assignment.note_number_for(note.pitch)
                if assignment is not None
                else midi_note_number(note.pitch)
            )
            start = _ticks(
                note.offset,
                ticks_per_beat=self.ticks_per_beat,
                field=f"note {note.pitch} offset",
            )
            end = _ticks(
                note.end,
                ticks_per_beat=self.ticks_per_beat,
                field=f"note {note.pitch} end",
            )
            events.extend(
                (
                    (
                        start,
                        1,
                        note_number,
                        Message(
                            "note_on",
                            note=note_number,
                            velocity=velocity,
                            channel=channel,
                        ),
                    ),
                    (
                        end,
                        0,
                        note_number,
                        Message(
                            "note_off",
                            note=note_number,
                            velocity=0,
                            channel=channel,
                        ),
                    ),
                )
            )

        return tuple(
            (tick, message)
            for tick, _, _, message in sorted(
                events,
                key=lambda event: (event[0], event[1], event[2]),
            )
        )
