"""Immutable progression of accepted composition snapshots."""

from dataclasses import dataclass

from prevox.domain.evaluation import AcceptanceDecision, Proposal
from prevox.domain.music import MusicIR


@dataclass(frozen=True, slots=True)
class CompositionState:
    """The accepted musical world at one revision."""

    revision: int = 0
    music: MusicIR | None = None
    decisions: tuple[AcceptanceDecision, ...] = ()

    def __post_init__(self) -> None:
        if (
            isinstance(self.revision, bool)
            or not isinstance(self.revision, int)
            or self.revision < 0
        ):
            raise ValueError("state revision must be a non-negative integer")
        if self.music is not None and not isinstance(self.music, MusicIR):
            raise TypeError("state music must be MusicIR or None")
        object.__setattr__(self, "decisions", tuple(self.decisions))
        if any(
            not isinstance(decision, AcceptanceDecision)
            for decision in self.decisions
        ):
            raise TypeError(
                "state decisions must all be AcceptanceDecision values"
            )

    def advance(
        self,
        proposal: Proposal,
        decision: AcceptanceDecision,
    ) -> "CompositionState":
        """Return the next state after one accepted, matching Proposal."""
        if proposal.identifier != decision.proposal_id:
            raise ValueError("decision does not refer to this proposal")
        if not decision.accepted:
            raise ValueError("a rejected proposal cannot advance state")
        return CompositionState(
            revision=self.revision + 1,
            music=proposal.candidate,
            decisions=(*self.decisions, decision),
        )
