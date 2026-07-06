"""Deterministic temporal transformations for Motif values."""

from fractions import Fraction

from prevox.domain._values import BeatLike, as_beat, require_identifier
from prevox.domain.music import Motif, Note


def _derived_identifier(identifier: str) -> str:
    return require_identifier(identifier, field="derived motif identifier")


def _ordered(notes: list[Note]) -> tuple[Note, ...]:
    return tuple(
        sorted(
            notes,
            key=lambda note: (
                note.offset,
                str(note.pitch),
                note.duration,
            ),
        )
    )


def reverse(motif: Motif, *, identifier: str) -> Motif:
    """Reflect note positions around the end of a Motif."""
    result_id = _derived_identifier(identifier)
    notes = [
        Note(
            pitch=note.pitch,
            offset=motif.duration - note.end,
            duration=note.duration,
        )
        for note in motif.notes
    ]
    return Motif(
        identifier=result_id,
        duration=motif.duration,
        notes=_ordered(notes),
    )


def repeat(motif: Motif, times: int, *, identifier: str) -> Motif:
    """Concatenate a Motif with itself an exact number of times."""
    result_id = _derived_identifier(identifier)
    if isinstance(times, bool) or not isinstance(times, int) or times < 1:
        raise ValueError("repeat times must be a positive integer")

    notes = [
        Note(
            pitch=note.pitch,
            offset=note.offset + motif.duration * iteration,
            duration=note.duration,
        )
        for iteration in range(times)
        for note in motif.notes
    ]
    return Motif(
        identifier=result_id,
        duration=motif.duration * times,
        notes=_ordered(notes),
    )


def scale_time(
    motif: Motif,
    factor: BeatLike,
    *,
    identifier: str,
) -> Motif:
    """Scale every offset and duration by one exact positive factor."""
    result_id = _derived_identifier(identifier)
    exact_factor = as_beat(factor, field="time scale", positive=True)
    notes = [
        Note(
            pitch=note.pitch,
            offset=note.offset * exact_factor,
            duration=note.duration * exact_factor,
        )
        for note in motif.notes
    ]
    return Motif(
        identifier=result_id,
        duration=motif.duration * exact_factor,
        notes=_ordered(notes),
    )


def augment(
    motif: Motif,
    *,
    identifier: str,
    factor: BeatLike = 2,
) -> Motif:
    """Lengthen a Motif by an exact factor greater than one."""
    exact_factor = as_beat(factor, field="augmentation factor", positive=True)
    if exact_factor <= 1:
        raise ValueError("augmentation factor must be greater than one")
    return scale_time(motif, exact_factor, identifier=identifier)


def diminish(
    motif: Motif,
    *,
    identifier: str,
    divisor: BeatLike = 2,
) -> Motif:
    """Shorten a Motif by an exact divisor greater than one."""
    exact_divisor = as_beat(
        divisor,
        field="diminution divisor",
        positive=True,
    )
    if exact_divisor <= 1:
        raise ValueError("diminution divisor must be greater than one")
    return scale_time(
        motif,
        Fraction(1, 1) / exact_divisor,
        identifier=identifier,
    )
