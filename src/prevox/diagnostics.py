"""Compiler-style diagnostics for inspectable composition workflows."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from prevox.domain._values import require_identifier


class DiagnosticSeverity(StrEnum):
    """The severity of a diagnostic emitted by a compiler-like workflow."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class DiagnosticLocation:
    """A stable domain path for a diagnostic.

    Locations deliberately name musical/domain objects instead of source lines
    because Prevox does not yet have a persisted DSL or file format.
    """

    path: tuple[str, ...]

    def __init__(self, path: Iterable[str]) -> None:
        normalized = tuple(
            require_identifier(part, field="diagnostic location part")
            for part in path
        )
        if not normalized:
            raise ValueError("diagnostic location path must not be empty")
        object.__setattr__(self, "path", normalized)

    def __str__(self) -> str:
        return " → ".join(self.path)


@dataclass(frozen=True, slots=True)
class Diagnostic:
    """A human-readable problem or note emitted by a pass or validator."""

    code: str
    severity: DiagnosticSeverity
    message: str
    location: DiagnosticLocation | None = None
    expected: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_identifier(self.code, field="diagnostic code")
        require_identifier(self.message, field="diagnostic message")
        if not isinstance(self.severity, DiagnosticSeverity):
            raise TypeError("diagnostic severity must be a DiagnosticSeverity")
        if self.location is not None and not isinstance(
            self.location,
            DiagnosticLocation,
        ):
            raise TypeError("diagnostic location must be DiagnosticLocation")
        if any(not isinstance(item, str) or not item.strip() for item in self.expected):
            raise ValueError("diagnostic expected values must be non-empty strings")
        if any(not isinstance(item, str) or not item.strip() for item in self.notes):
            raise ValueError("diagnostic notes must be non-empty strings")


@dataclass(frozen=True, slots=True)
class DiagnosticReport:
    """An immutable collection of diagnostics from one compiler-like step."""

    diagnostics: tuple[Diagnostic, ...] = ()

    def __init__(self, diagnostics: Iterable[Diagnostic] = ()) -> None:
        normalized = tuple(diagnostics)
        if any(not isinstance(item, Diagnostic) for item in normalized):
            raise TypeError("diagnostic report entries must be Diagnostic values")
        object.__setattr__(self, "diagnostics", normalized)

    @property
    def errors(self) -> tuple[Diagnostic, ...]:
        """Return the diagnostics that should block accepting a proposal."""
        return tuple(
            diagnostic
            for diagnostic in self.diagnostics
            if diagnostic.severity is DiagnosticSeverity.ERROR
        )

    @property
    def has_errors(self) -> bool:
        """Whether this report contains any blocking diagnostic."""
        return bool(self.errors)

    @property
    def is_success(self) -> bool:
        """Whether the report contains no blocking diagnostics."""
        return not self.has_errors

    def add(self, diagnostic: Diagnostic) -> "DiagnosticReport":
        """Return a new report with one more diagnostic."""
        if not isinstance(diagnostic, Diagnostic):
            raise TypeError("diagnostic must be a Diagnostic")
        return DiagnosticReport((*self.diagnostics, diagnostic))

    def extend(self, diagnostics: Iterable[Diagnostic]) -> "DiagnosticReport":
        """Return a new report with additional diagnostics."""
        return DiagnosticReport((*self.diagnostics, *tuple(diagnostics)))
