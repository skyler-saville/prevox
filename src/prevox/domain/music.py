"""Backend-independent symbolic music with exact relative time."""

from dataclasses import dataclass
from enum import StrEnum
from fractions import Fraction
import re
from typing import Generic, Iterable, Iterator, Protocol, TypeVar

from prevox.domain._values import (
    Beat,
    BeatLike,
    as_beat,
    require_identifier,
)

_PITCH_CLASS = re.compile(r"^(?P<step>[A-G])(?P<accidental>bb|b|#|##)?$")
_PITCH = re.compile(
    r"^(?P<step>[A-G])(?P<accidental>bb|b|#|##)?(?P<octave>-?[0-9]+)$"
)
_ACCIDENTALS = {"": 0, "b": -1, "bb": -2, "#": 1, "##": 2}
_ACCIDENTAL_NAMES = {value: key for key, value in _ACCIDENTALS.items()}


@dataclass(frozen=True, slots=True, order=True)
class PitchClass:
    """An enharmonically spelled pitch class, independent of MIDI numbers."""

    step: str
    accidental: int = 0

    def __post_init__(self) -> None:
        if self.step not in "ABCDEFG" or len(self.step) != 1:
            raise ValueError("pitch-class step must be one of A through G")
        if self.accidental not in _ACCIDENTAL_NAMES:
            raise ValueError("pitch-class accidental must be between -2 and 2")

    @classmethod
    def parse(cls, value: str) -> "PitchClass":
        """Parse a pitch class such as D, F#, or E-flat spelled as Eb."""
        match = _PITCH_CLASS.fullmatch(value)
        if match is None:
            raise ValueError(f"invalid pitch class: {value!r}")
        accidental = match.group("accidental") or ""
        return cls(match.group("step"), _ACCIDENTALS[accidental])

    def __str__(self) -> str:
        return f"{self.step}{_ACCIDENTAL_NAMES[self.accidental]}"


@dataclass(frozen=True, slots=True, order=True)
class Pitch:
    """A spelled pitch with octave, independent of any transport encoding."""

    pitch_class: PitchClass
    octave: int

    def __post_init__(self) -> None:
        if isinstance(self.octave, bool) or not isinstance(self.octave, int):
            raise TypeError("pitch octave must be an integer")

    @classmethod
    def parse(cls, value: str) -> "Pitch":
        """Parse a pitch such as D4, F#3, or Eb-1."""
        match = _PITCH.fullmatch(value)
        if match is None:
            raise ValueError(f"invalid pitch: {value!r}")
        accidental = match.group("accidental") or ""
        return cls(
            PitchClass(match.group("step"), _ACCIDENTALS[accidental]),
            int(match.group("octave")),
        )

    def __str__(self) -> str:
        return f"{self.pitch_class}{self.octave}"


@dataclass(frozen=True, slots=True)
class TonalContext:
    """A tonic and named mode without embedding a theory catalog."""

    tonic: PitchClass
    mode: str

    def __post_init__(self) -> None:
        require_identifier(self.mode, field="mode")

    def __str__(self) -> str:
        return f"{self.tonic} {self.mode}"


@dataclass(frozen=True, slots=True)
class Note:
    """A symbolic pitched event in local motif time."""

    pitch: Pitch
    offset: Beat
    duration: Beat

    def __init__(
        self,
        pitch: Pitch,
        offset: BeatLike,
        duration: BeatLike,
    ) -> None:
        if not isinstance(pitch, Pitch):
            raise TypeError("note pitch must be a Pitch")
        object.__setattr__(self, "pitch", pitch)
        object.__setattr__(
            self,
            "offset",
            as_beat(offset, field="note offset"),
        )
        object.__setattr__(
            self,
            "duration",
            as_beat(duration, field="note duration", positive=True),
        )

    @property
    def end(self) -> Beat:
        return self.offset + self.duration


class HasDuration(Protocol):
    """A value that can be placed on a parent timeline."""

    @property
    def duration(self) -> Beat: ...


T = TypeVar("T", bound=HasDuration)


@dataclass(frozen=True, slots=True)
class Placement(Generic[T]):
    """Place a reusable value at an exact offset in its parent."""

    item: T
    offset: Beat

    def __init__(self, item: T, offset: BeatLike) -> None:
        if not hasattr(item, "duration"):
            raise TypeError("placed item must expose a duration")
        object.__setattr__(self, "item", item)
        object.__setattr__(
            self,
            "offset",
            as_beat(offset, field="placement offset"),
        )

    @property
    def end(self) -> Beat:
        return self.offset + self.item.duration


def _as_tuple(values: Iterable[T]) -> tuple[T, ...]:
    return tuple(values)


def _validate_unique_identifiers(
    values: Iterable[object],
    *,
    kind: str,
) -> None:
    identifiers = [getattr(value, "identifier") for value in values]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError(f"{kind} identifiers must be unique")


def _validate_placements_fit(
    placements: Iterable[Placement[HasDuration]],
    *,
    duration: Beat,
    parent: str,
) -> None:
    for placement in placements:
        if placement.end > duration:
            raise ValueError(
                f"{parent} placement at {placement.offset} ends at "
                f"{placement.end}, beyond duration {duration}"
            )


@dataclass(frozen=True, slots=True)
class Motif:
    """A reusable note relationship in local time."""

    identifier: str
    duration: Beat
    notes: tuple[Note, ...]

    def __init__(
        self,
        identifier: str,
        duration: BeatLike,
        notes: Iterable[Note],
    ) -> None:
        object.__setattr__(
            self,
            "identifier",
            require_identifier(identifier, field="motif identifier"),
        )
        exact_duration = as_beat(
            duration,
            field="motif duration",
            positive=True,
        )
        object.__setattr__(self, "duration", exact_duration)
        normalized_notes = _as_tuple(notes)
        if not normalized_notes:
            raise ValueError("motif must contain at least one note")
        if any(not isinstance(note, Note) for note in normalized_notes):
            raise TypeError("motif notes must all be Note values")
        if any(note.end > exact_duration for note in normalized_notes):
            raise ValueError("motif note extends beyond motif duration")
        object.__setattr__(self, "notes", normalized_notes)


@dataclass(frozen=True, slots=True)
class Phrase:
    """A bounded musical unit made from placed motifs."""

    identifier: str
    duration: Beat
    motifs: tuple[Placement[Motif], ...]

    def __init__(
        self,
        identifier: str,
        duration: BeatLike,
        motifs: Iterable[Placement[Motif]],
    ) -> None:
        object.__setattr__(
            self,
            "identifier",
            require_identifier(identifier, field="phrase identifier"),
        )
        exact_duration = as_beat(
            duration,
            field="phrase duration",
            positive=True,
        )
        object.__setattr__(self, "duration", exact_duration)
        normalized_motifs = _as_tuple(motifs)
        if any(
            not isinstance(placement, Placement)
            or not isinstance(placement.item, Motif)
            for placement in normalized_motifs
        ):
            raise TypeError("phrase placements must contain Motif values")
        _validate_placements_fit(
            normalized_motifs,
            duration=exact_duration,
            parent="phrase",
        )
        object.__setattr__(self, "motifs", normalized_motifs)


class VoiceRole(StrEnum):
    """A logical compositional responsibility, not an instrument."""

    LEAD = "lead"
    BASS = "bass"
    HARMONY = "harmony"
    PULSE = "pulse"
    TEXTURE = "texture"


@dataclass(frozen=True, slots=True)
class Voice:
    """A logical timeline of phrases within a section."""

    identifier: str
    role: VoiceRole
    phrases: tuple[Placement[Phrase], ...]
    max_polyphony: int = 1

    def __init__(
        self,
        identifier: str,
        role: VoiceRole,
        phrases: Iterable[Placement[Phrase]],
        max_polyphony: int = 1,
    ) -> None:
        object.__setattr__(
            self,
            "identifier",
            require_identifier(identifier, field="voice identifier"),
        )
        if not isinstance(role, VoiceRole):
            raise TypeError("voice role must be a VoiceRole")
        object.__setattr__(self, "role", role)
        if (
            isinstance(max_polyphony, bool)
            or not isinstance(max_polyphony, int)
            or max_polyphony < 1
        ):
            raise ValueError("max_polyphony must be a positive integer")
        object.__setattr__(self, "max_polyphony", max_polyphony)

        normalized_phrases = _as_tuple(phrases)
        if any(
            not isinstance(placement, Placement)
            or not isinstance(placement.item, Phrase)
            for placement in normalized_phrases
        ):
            raise TypeError("voice placements must contain Phrase values")
        object.__setattr__(self, "phrases", normalized_phrases)


@dataclass(frozen=True, slots=True)
class Section:
    """A formal span containing logical voices."""

    identifier: str
    duration: Beat
    voices: tuple[Voice, ...]

    def __init__(
        self,
        identifier: str,
        duration: BeatLike,
        voices: Iterable[Voice],
    ) -> None:
        object.__setattr__(
            self,
            "identifier",
            require_identifier(identifier, field="section identifier"),
        )
        exact_duration = as_beat(
            duration,
            field="section duration",
            positive=True,
        )
        object.__setattr__(self, "duration", exact_duration)
        normalized_voices = _as_tuple(voices)
        if any(not isinstance(voice, Voice) for voice in normalized_voices):
            raise TypeError("section voices must all be Voice values")
        _validate_unique_identifiers(normalized_voices, kind="voice")
        for voice in normalized_voices:
            _validate_placements_fit(
                voice.phrases,
                duration=exact_duration,
                parent=f"voice {voice.identifier!r}",
            )
        object.__setattr__(self, "voices", normalized_voices)


@dataclass(frozen=True, slots=True)
class Song:
    """The aggregate root for a realized symbolic composition."""

    identifier: str
    title: str
    duration: Beat
    tempo_bpm: int
    tonal_context: TonalContext
    sections: tuple[Placement[Section], ...]

    def __init__(
        self,
        identifier: str,
        title: str,
        duration: BeatLike,
        tempo_bpm: int,
        tonal_context: TonalContext,
        sections: Iterable[Placement[Section]],
    ) -> None:
        object.__setattr__(
            self,
            "identifier",
            require_identifier(identifier, field="song identifier"),
        )
        object.__setattr__(
            self,
            "title",
            require_identifier(title, field="song title"),
        )
        exact_duration = as_beat(
            duration,
            field="song duration",
            positive=True,
        )
        object.__setattr__(self, "duration", exact_duration)
        if (
            isinstance(tempo_bpm, bool)
            or not isinstance(tempo_bpm, int)
            or tempo_bpm <= 0
        ):
            raise ValueError("tempo_bpm must be a positive integer")
        object.__setattr__(self, "tempo_bpm", tempo_bpm)
        if not isinstance(tonal_context, TonalContext):
            raise TypeError("tonal_context must be a TonalContext")
        object.__setattr__(self, "tonal_context", tonal_context)

        normalized_sections = _as_tuple(sections)
        if any(
            not isinstance(placement, Placement)
            or not isinstance(placement.item, Section)
            for placement in normalized_sections
        ):
            raise TypeError("song placements must contain Section values")
        _validate_placements_fit(
            normalized_sections,
            duration=exact_duration,
            parent="song",
        )
        _validate_unique_identifiers(
            (placement.item for placement in normalized_sections),
            kind="section",
        )
        object.__setattr__(self, "sections", normalized_sections)


@dataclass(frozen=True, slots=True)
class RealizedNote:
    """A derived absolute-time view over one symbolic note."""

    section_id: str
    voice_id: str
    phrase_id: str
    motif_id: str
    pitch: Pitch
    offset: Beat
    duration: Beat

    @property
    def end(self) -> Beat:
        return self.offset + self.duration


@dataclass(frozen=True, slots=True)
class MusicIR:
    """The canonical realized symbolic representation."""

    song: Song
    schema_version: str = "0.1"

    def __post_init__(self) -> None:
        if not isinstance(self.song, Song):
            raise TypeError("MusicIR song must be a Song")
        require_identifier(self.schema_version, field="MusicIR schema version")
        self._validate_polyphony()

    def iter_notes(self) -> Iterator[RealizedNote]:
        """Yield a flattened view by composing every local placement."""
        for section_placement in self.song.sections:
            section = section_placement.item
            for voice in section.voices:
                for phrase_placement in voice.phrases:
                    phrase = phrase_placement.item
                    for motif_placement in phrase.motifs:
                        motif = motif_placement.item
                        base = (
                            section_placement.offset
                            + phrase_placement.offset
                            + motif_placement.offset
                        )
                        for note in motif.notes:
                            yield RealizedNote(
                                section_id=section.identifier,
                                voice_id=voice.identifier,
                                phrase_id=phrase.identifier,
                                motif_id=motif.identifier,
                                pitch=note.pitch,
                                offset=base + note.offset,
                                duration=note.duration,
                            )

    def _validate_polyphony(self) -> None:
        voices: dict[str, tuple[int, list[RealizedNote]]] = {}
        voice_limits = {
            voice.identifier: voice.max_polyphony
            for placement in self.song.sections
            for voice in placement.item.voices
        }
        for note in self.iter_notes():
            limit, notes = voices.setdefault(
                note.voice_id,
                (voice_limits[note.voice_id], []),
            )
            notes.append(note)
            voices[note.voice_id] = (limit, notes)

        for voice_id, (limit, notes) in voices.items():
            boundaries = sorted(
                [
                    boundary
                    for note in notes
                    for boundary in (
                        (note.offset, 1),
                        (note.end, -1),
                    )
                ],
                key=lambda boundary: (boundary[0], boundary[1]),
            )
            active = 0
            for _, change in boundaries:
                active += change
                if active > limit:
                    raise ValueError(
                        f"voice {voice_id!r} exceeds max_polyphony {limit}"
                    )
