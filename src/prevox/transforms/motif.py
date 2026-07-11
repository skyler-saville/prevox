"""Deterministic temporal transformations for Motif values."""

from fractions import Fraction

from prevox.diagnostics import (
    Diagnostic,
    DiagnosticLocation,
    DiagnosticReport,
    DiagnosticSeverity,
)
from prevox.domain._values import BeatLike, as_beat, require_identifier
from prevox.domain.music import Motif, Note


def _motif_location(motif: object) -> DiagnosticLocation | None:
    if isinstance(motif, Motif):
        return DiagnosticLocation((f"Motif {motif.identifier!r}",))
    return None


def _diagnose_motif(motif: object, *, transform: str) -> tuple[Diagnostic, ...]:
    if isinstance(motif, Motif):
        return ()
    return (
        Diagnostic(
            code="transform.invalid_motif",
            severity=DiagnosticSeverity.ERROR,
            message=f"{transform} requires a Motif value",
            expected=("motif is a prevox.domain.Motif",),
        ),
    )


def _diagnose_identifier(identifier: object) -> tuple[Diagnostic, ...]:
    if isinstance(identifier, str) and identifier.strip():
        return ()
    return (
        Diagnostic(
            code="transform.invalid_identifier",
            severity=DiagnosticSeverity.ERROR,
            message="derived motif identifier is required",
            expected=("identifier is a non-empty string",),
        ),
    )


def diagnose_repeat(
    motif: object,
    times: object,
    *,
    identifier: object,
) -> DiagnosticReport:
    """Return diagnostics for a repeat transform without raising."""
    diagnostics = [
        *_diagnose_motif(motif, transform="repeat"),
        *_diagnose_identifier(identifier),
    ]
    if isinstance(times, bool) or not isinstance(times, int) or times < 1:
        diagnostics.append(
            Diagnostic(
                code="transform.invalid_repeat_count",
                severity=DiagnosticSeverity.ERROR,
                message=f"cannot repeat by {times!r}",
                location=_motif_location(motif),
                expected=("times is a positive integer",),
            )
        )
    return DiagnosticReport(diagnostics)


def diagnose_scale_time(
    motif: object,
    factor: object,
    *,
    identifier: object,
) -> DiagnosticReport:
    """Return diagnostics for a time-scaling transform without raising."""
    diagnostics = [
        *_diagnose_motif(motif, transform="scale_time"),
        *_diagnose_identifier(identifier),
    ]
    if isinstance(factor, bool) or not isinstance(factor, (int, Fraction)):
        diagnostics.append(
            Diagnostic(
                code="transform.invalid_time_scale",
                severity=DiagnosticSeverity.ERROR,
                message=f"cannot scale time by {factor!r}",
                location=_motif_location(motif),
                expected=("factor is an int or Fraction",),
                notes=("floating-point factors are rejected to preserve exact time",),
            )
        )
    elif Fraction(factor) <= 0:
        diagnostics.append(
            Diagnostic(
                code="transform.invalid_time_scale",
                severity=DiagnosticSeverity.ERROR,
                message=f"cannot scale time by {factor!r}",
                location=_motif_location(motif),
                expected=("factor is greater than zero",),
            )
        )
    return DiagnosticReport(diagnostics)


def diagnose_augment(
    motif: object,
    *,
    identifier: object,
    factor: object = 2,
) -> DiagnosticReport:
    """Return diagnostics for an augmentation transform without raising."""
    report = diagnose_scale_time(motif, factor, identifier=identifier)
    diagnostics = list(report.diagnostics)
    if isinstance(factor, bool) or not isinstance(factor, (int, Fraction)):
        return DiagnosticReport(diagnostics)
    if Fraction(factor) <= 1:
        diagnostics.append(
            Diagnostic(
                code="transform.invalid_augmentation_factor",
                severity=DiagnosticSeverity.ERROR,
                message=f"cannot augment by {factor!r}",
                location=_motif_location(motif),
                expected=("factor is greater than one",),
            )
        )
    return DiagnosticReport(diagnostics)


def diagnose_diminish(
    motif: object,
    *,
    identifier: object,
    divisor: object = 2,
) -> DiagnosticReport:
    """Return diagnostics for a diminution transform without raising."""
    diagnostics = [
        *_diagnose_motif(motif, transform="diminish"),
        *_diagnose_identifier(identifier),
    ]
    if isinstance(divisor, bool) or not isinstance(divisor, (int, Fraction)):
        diagnostics.append(
            Diagnostic(
                code="transform.invalid_diminution_divisor",
                severity=DiagnosticSeverity.ERROR,
                message=f"cannot diminish by {divisor!r}",
                location=_motif_location(motif),
                expected=("divisor is an int or Fraction greater than one",),
            )
        )
    elif Fraction(divisor) <= 1:
        diagnostics.append(
            Diagnostic(
                code="transform.invalid_diminution_divisor",
                severity=DiagnosticSeverity.ERROR,
                message=f"cannot diminish by {divisor!r}",
                location=_motif_location(motif),
                expected=("divisor is greater than one",),
            )
        )
    return DiagnosticReport(diagnostics)


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
