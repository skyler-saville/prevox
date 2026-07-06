"""Shared value validation helpers."""

from fractions import Fraction
from typing import TypeAlias

Beat: TypeAlias = Fraction
BeatLike: TypeAlias = int | Fraction


def as_beat(value: BeatLike, *, field: str, positive: bool = False) -> Beat:
    """Return an exact beat value and reject lossy floating-point input."""
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{field} must be an int or Fraction")

    beat = Fraction(value)
    if positive and beat <= 0:
        raise ValueError(f"{field} must be greater than zero")
    if not positive and beat < 0:
        raise ValueError(f"{field} must be zero or greater")
    return beat


def require_identifier(value: str, *, field: str) -> str:
    """Validate a stable, human-readable identifier."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def require_probability(value: float, *, field: str) -> float:
    """Validate a normalized score or confidence."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field} must be numeric")
    normalized = float(value)
    if not 0.0 <= normalized <= 1.0:
        raise ValueError(f"{field} must be between 0.0 and 1.0")
    return normalized
