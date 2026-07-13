"""Small backend-independent theory helpers for analysis passes."""

from dataclasses import dataclass
from typing import Iterable

from prevox.domain import Pitch, PitchClass, TonalContext

_PITCH_CLASS_CHROMA = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
}

_MODE_INTERVALS = {
    "ionian": (0, 2, 4, 5, 7, 9, 11),
    "dorian": (0, 2, 3, 5, 7, 9, 10),
    "phrygian": (0, 1, 3, 5, 7, 8, 10),
    "lydian": (0, 2, 4, 6, 7, 9, 11),
    "mixolydian": (0, 2, 4, 5, 7, 9, 10),
    "aeolian": (0, 2, 3, 5, 7, 8, 10),
    "locrian": (0, 1, 3, 5, 6, 8, 10),
    "major": (0, 2, 4, 5, 7, 9, 11),
    "minor": (0, 2, 3, 5, 7, 8, 10),
}

PREVIEW_PERCUSSION_PITCHES = frozenset(
    Pitch.parse(value)
    for value in (
        "C2",
        "D2",
        "F#2",
        "G#2",
        "C#3",
        "D#3",
    )
)

STABLE_VERTICAL_INTERVAL_CHROMAS = frozenset({0, 5, 7})


@dataclass(frozen=True, slots=True)
class Scale:
    """An ordered chromatic pitch-class collection rooted on a tonic."""

    tonal_context: TonalContext
    chromas: tuple[int, ...]

    def contains(self, pitch: Pitch) -> bool:
        """Whether a pitch belongs to this scale by chromatic pitch class."""
        return pitch_chroma(pitch) in self.chromas


def pitch_class_chroma(pitch_class: PitchClass) -> int:
    """Return a 12-TET chroma for a spelled pitch class, independent of MIDI."""
    if not isinstance(pitch_class, PitchClass):
        raise TypeError("pitch_class must be a PitchClass")
    return (
        _PITCH_CLASS_CHROMA[pitch_class.step] + pitch_class.accidental
    ) % 12


def pitch_chroma(pitch: Pitch) -> int:
    """Return a 12-TET chroma for a spelled pitch, independent of octave."""
    if not isinstance(pitch, Pitch):
        raise TypeError("pitch must be a Pitch")
    return pitch_class_chroma(pitch.pitch_class)


def build_scale(tonal_context: TonalContext) -> Scale:
    """Build the scale implied by a supported tonal context."""
    if not isinstance(tonal_context, TonalContext):
        raise TypeError("tonal_context must be a TonalContext")
    mode = tonal_context.mode.casefold()
    if mode not in _MODE_INTERVALS:
        raise ValueError(f"unsupported tonal context mode: {tonal_context.mode}")
    tonic = pitch_class_chroma(tonal_context.tonic)
    return Scale(
        tonal_context=tonal_context,
        chromas=tuple((tonic + interval) % 12 for interval in _MODE_INTERVALS[mode]),
    )


def vertical_interval_chroma(lower: Pitch, upper: Pitch) -> int:
    """Return the directed chromatic interval class from lower to upper."""
    return (absolute_pitch_chroma(upper) - absolute_pitch_chroma(lower)) % 12


def absolute_pitch_chroma(pitch: Pitch) -> int:
    """Return a chromatic pitch number without assigning MIDI transport meaning."""
    if not isinstance(pitch, Pitch):
        raise TypeError("pitch must be a Pitch")
    return (pitch.octave + 1) * 12 + pitch_chroma(pitch)


def is_stable_vertical_interval(lower: Pitch, upper: Pitch) -> bool:
    """Whether two simultaneous pitches form a simple stable preview interval."""
    return vertical_interval_chroma(lower, upper) in STABLE_VERTICAL_INTERVAL_CHROMAS


def all_preview_percussion(pitches: Iterable[Pitch]) -> bool:
    """Whether all pitches belong to the temporary GM drum preview convention."""
    normalized = tuple(pitches)
    return bool(normalized) and all(
        pitch in PREVIEW_PERCUSSION_PITCHES for pitch in normalized
    )
