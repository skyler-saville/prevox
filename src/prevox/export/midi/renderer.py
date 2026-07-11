"""Minimal Standard MIDI File export for Music IR.

This renderer intentionally owns the temporary 12-TET preview mapping, velocity,
channel, and ticks-per-beat choices. Those concepts must not leak into Music IR.
"""

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import BinaryIO

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

from prevox.domain import MusicIR, Pitch

_PITCH_CLASS_TO_SEMITONE = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
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


@dataclass(frozen=True, slots=True)
class MidiRenderer:
    """Write Music IR to a deterministic Standard MIDI File."""

    ticks_per_beat: int = 480
    preview_velocity: int = 64
    channel: int = 0

    def __post_init__(self) -> None:
        if (
            isinstance(self.ticks_per_beat, bool)
            or not isinstance(self.ticks_per_beat, int)
            or self.ticks_per_beat <= 0
        ):
            raise ValueError("ticks_per_beat must be a positive integer")
        if (
            isinstance(self.preview_velocity, bool)
            or not isinstance(self.preview_velocity, int)
            or not 1 <= self.preview_velocity <= 127
        ):
            raise ValueError("preview_velocity must be between 1 and 127")
        if (
            isinstance(self.channel, bool)
            or not isinstance(self.channel, int)
            or not 0 <= self.channel <= 15
        ):
            raise ValueError("channel must be between 0 and 15")

    def to_midi_file(self, music: MusicIR) -> MidiFile:
        """Return an in-memory Standard MIDI File for one Music IR value."""
        if not isinstance(music, MusicIR):
            raise TypeError("music must be a MusicIR")

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

        last_tick = 0
        for tick, message in self._messages(music):
            message.time = tick - last_tick
            track.append(message)
            last_tick = tick
        track.append(MetaMessage("end_of_track", time=0))
        return midi

    def write(self, music: MusicIR, path: str | Path | BinaryIO) -> None:
        """Write Music IR to a Standard MIDI File path or binary file."""
        if isinstance(path, (str, Path)):
            target = Path(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            self.to_midi_file(music).save(target)
            return
        self.to_midi_file(music).save(file=path)

    def _messages(self, music: MusicIR) -> tuple[tuple[int, Message], ...]:
        events: list[tuple[int, int, int, Message]] = []
        for note in music.iter_notes():
            note_number = midi_note_number(note.pitch)
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
                            velocity=self.preview_velocity,
                            channel=self.channel,
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
                            channel=self.channel,
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
