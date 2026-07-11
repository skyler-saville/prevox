"""Proposal rationale, independent criticism, and acceptance records."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from prevox.domain._values import require_identifier, require_probability
from prevox.domain.music import MusicIR


@dataclass(frozen=True, slots=True)
class PredictedEffect:
    """A Composer's prediction, not an independent measurement."""

    name: str
    delta: float
    confidence: float

    def __post_init__(self) -> None:
        require_identifier(self.name, field="predicted effect name")
        if isinstance(self.delta, bool) or not isinstance(
            self.delta,
            (int, float),
        ):
            raise TypeError("predicted effect delta must be numeric")
        object.__setattr__(self, "delta", float(self.delta))
        object.__setattr__(
            self,
            "confidence",
            require_probability(
                self.confidence,
                field="predicted effect confidence",
            ),
        )


@dataclass(frozen=True, slots=True)
class ProposalRationale:
    """Structured evidence about why a candidate was proposed."""

    summary: str
    objectives: tuple[str, ...] = ()
    predicted_effects: tuple[PredictedEffect, ...] = ()

    def __init__(
        self,
        summary: str,
        objectives: Iterable[str] = (),
        predicted_effects: Iterable[PredictedEffect] = (),
    ) -> None:
        object.__setattr__(
            self,
            "summary",
            require_identifier(summary, field="proposal rationale"),
        )
        object.__setattr__(
            self,
            "objectives",
            tuple(
                require_identifier(objective, field="proposal objective")
                for objective in objectives
            ),
        )
        object.__setattr__(
            self,
            "predicted_effects",
            tuple(predicted_effects),
        )
        if any(
            not isinstance(effect, PredictedEffect)
            for effect in self.predicted_effects
        ):
            raise TypeError(
                "predicted_effects must all be PredictedEffect values"
            )


@dataclass(frozen=True, slots=True)
class Proposal:
    """One immutable candidate realization of an Intent."""

    identifier: str
    intent_id: str
    candidate: MusicIR
    rationale: ProposalRationale

    def __post_init__(self) -> None:
        require_identifier(self.identifier, field="proposal identifier")
        require_identifier(self.intent_id, field="proposal intent identifier")
        if not isinstance(self.candidate, MusicIR):
            raise TypeError("proposal candidate must be MusicIR")
        if not isinstance(self.rationale, ProposalRationale):
            raise TypeError("proposal rationale must be ProposalRationale")


@dataclass(frozen=True, slots=True)
class Measurement:
    """One named observation made by a Critic."""

    name: str
    value: float

    def __post_init__(self) -> None:
        require_identifier(self.name, field="measurement name")
        if isinstance(self.value, bool) or not isinstance(
            self.value,
            (int, float),
        ):
            raise TypeError("measurement value must be numeric")
        object.__setattr__(self, "value", float(self.value))


class CritiqueVerdict(StrEnum):
    """A recommendation that remains separate from hard IR validity."""

    SUPPORT = "support"
    OPPOSE = "oppose"
    ABSTAIN = "abstain"


@dataclass(frozen=True, slots=True)
class Critique:
    """An independent, evidence-bearing judgment of a Proposal."""

    identifier: str
    critic: str
    proposal_id: str
    verdict: CritiqueVerdict
    confidence: float
    measurements: tuple[Measurement, ...] = ()
    evidence: tuple[str, ...] = ()
    reservations: tuple[str, ...] = ()

    def __init__(
        self,
        identifier: str,
        critic: str,
        proposal_id: str,
        verdict: CritiqueVerdict,
        confidence: float,
        measurements: Iterable[Measurement] = (),
        evidence: Iterable[str] = (),
        reservations: Iterable[str] = (),
    ) -> None:
        object.__setattr__(
            self,
            "identifier",
            require_identifier(identifier, field="critique identifier"),
        )
        object.__setattr__(
            self,
            "critic",
            require_identifier(critic, field="critic name"),
        )
        object.__setattr__(
            self,
            "proposal_id",
            require_identifier(proposal_id, field="critique proposal"),
        )
        if not isinstance(verdict, CritiqueVerdict):
            raise TypeError("critique verdict must be a CritiqueVerdict")
        object.__setattr__(self, "verdict", verdict)
        object.__setattr__(
            self,
            "confidence",
            require_probability(confidence, field="critique confidence"),
        )
        object.__setattr__(self, "measurements", tuple(measurements))
        if any(
            not isinstance(measurement, Measurement)
            for measurement in self.measurements
        ):
            raise TypeError("measurements must all be Measurement values")
        object.__setattr__(
            self,
            "evidence",
            tuple(
                require_identifier(item, field="critique evidence")
                for item in evidence
            ),
        )
        object.__setattr__(
            self,
            "reservations",
            tuple(
                require_identifier(item, field="critique reservation")
                for item in reservations
            ),
        )


@dataclass(frozen=True, slots=True)
class AcceptanceDecision:
    """The auditable result of applying one explicit policy."""

    proposal_id: str
    accepted: bool
    policy: str
    reason: str
    critique_ids: tuple[str, ...] = ()
    human_override: bool = False

    def __init__(
        self,
        proposal_id: str,
        accepted: bool,
        policy: str,
        reason: str,
        critique_ids: Iterable[str] = (),
        human_override: bool = False,
    ) -> None:
        object.__setattr__(
            self,
            "proposal_id",
            require_identifier(proposal_id, field="decision proposal"),
        )
        if not isinstance(accepted, bool):
            raise TypeError("accepted must be a bool")
        object.__setattr__(self, "accepted", accepted)
        object.__setattr__(
            self,
            "policy",
            require_identifier(policy, field="acceptance policy"),
        )
        object.__setattr__(
            self,
            "reason",
            require_identifier(reason, field="acceptance reason"),
        )
        object.__setattr__(
            self,
            "critique_ids",
            tuple(
                require_identifier(item, field="decision critique")
                for item in critique_ids
            ),
        )
        if len(self.critique_ids) != len(set(self.critique_ids)):
            raise ValueError("decision critique identifiers must be unique")
        if not isinstance(human_override, bool):
            raise TypeError("human_override must be a bool")
        object.__setattr__(self, "human_override", human_override)
