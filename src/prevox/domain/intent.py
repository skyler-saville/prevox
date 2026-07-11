"""High-level musical purpose, independent of realized notes."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from prevox.domain._values import (
    Beat,
    BeatLike,
    as_beat,
    require_identifier,
    require_probability,
)


class RhetoricalRole(StrEnum):
    """The discourse function requested of a musical span."""

    QUESTION = "question"
    ANSWER = "answer"
    ESCALATION = "escalation"
    TRANSITION = "transition"
    RESOLUTION = "resolution"


@dataclass(frozen=True, slots=True)
class IntentTarget:
    """A normalized, measurable goal such as energy or density."""

    name: str
    value: float

    def __post_init__(self) -> None:
        require_identifier(self.name, field="target name")
        object.__setattr__(
            self,
            "value",
            require_probability(self.value, field=f"target {self.name!r}"),
        )


@dataclass(frozen=True, slots=True)
class Intent:
    """A bounded request for one piece of musical behavior."""

    identifier: str
    role: RhetoricalRole
    duration: Beat
    targets: tuple[IntentTarget, ...] = ()
    preserve: tuple[str, ...] = ()

    def __init__(
        self,
        identifier: str,
        role: RhetoricalRole,
        duration: BeatLike,
        targets: Iterable[IntentTarget] = (),
        preserve: Iterable[str] = (),
    ) -> None:
        object.__setattr__(
            self,
            "identifier",
            require_identifier(identifier, field="intent identifier"),
        )
        if not isinstance(role, RhetoricalRole):
            raise TypeError("role must be a RhetoricalRole")
        object.__setattr__(self, "role", role)
        object.__setattr__(
            self,
            "duration",
            as_beat(duration, field="intent duration", positive=True),
        )

        normalized_targets = tuple(targets)
        if any(
            not isinstance(target, IntentTarget)
            for target in normalized_targets
        ):
            raise TypeError("intent targets must all be IntentTarget values")
        target_names = [target.name for target in normalized_targets]
        if len(target_names) != len(set(target_names)):
            raise ValueError("intent target names must be unique")
        object.__setattr__(self, "targets", normalized_targets)

        preserved = tuple(
            require_identifier(value, field="preserved relationship")
            for value in preserve
        )
        object.__setattr__(self, "preserve", preserved)

    def target(self, name: str) -> float | None:
        """Return a named target without exposing a mutable property bag."""
        return next(
            (target.value for target in self.targets if target.name == name),
            None,
        )
