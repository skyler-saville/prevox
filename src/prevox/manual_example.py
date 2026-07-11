"""A manual, deterministic architecture trace with no Composer or renderer."""

from dataclasses import dataclass

from prevox.domain import (
    AcceptanceDecision,
    CompositionState,
    Critique,
    CritiqueVerdict,
    Intent,
    IntentTarget,
    Measurement,
    MusicIR,
    Motif,
    Note,
    Phrase,
    Pitch,
    PitchClass,
    Placement,
    PredictedEffect,
    Proposal,
    ProposalRationale,
    RhetoricalRole,
    Section,
    Song,
    TonalContext,
    Voice,
    VoiceRole,
)
from prevox.inspection import format_trace


@dataclass(frozen=True, slots=True)
class ManualTrace:
    """All values in the hand-built pipeline, retained for tests and inspection."""

    intent: Intent
    proposal: Proposal
    critique: Critique
    decision: AcceptanceDecision
    state: CompositionState

    def format(self) -> str:
        return format_trace(
            intent=self.intent,
            proposal=self.proposal,
            critiques=(self.critique,),
            decision=self.decision,
            state=self.state,
        )


def build_manual_trace() -> ManualTrace:
    """Construct and accept eight bars of hard-coded D Dorian melody."""
    intent = Intent(
        identifier="dorian-escalation",
        role=RhetoricalRole.ESCALATION,
        duration=32,
        targets=(
            IntentTarget("energy", 0.65),
            IntentTarget("density", 0.25),
        ),
        preserve=("motif-a interval contour",),
    )

    motif = Motif(
        identifier="motif-a",
        duration=4,
        notes=(
            Note(Pitch.parse("D4"), offset=0, duration=1),
            Note(Pitch.parse("F4"), offset=1, duration=1),
            Note(Pitch.parse("G4"), offset=2, duration=1),
            Note(Pitch.parse("A4"), offset=3, duration=1),
        ),
    )
    phrase = Phrase(
        identifier="eight-bar-riff",
        duration=32,
        motifs=tuple(Placement(motif, offset) for offset in range(0, 32, 4)),
    )
    voice = Voice(
        identifier="lead",
        role=VoiceRole.LEAD,
        phrases=(Placement(phrase, 0),),
    )
    section = Section(
        identifier="verse",
        duration=32,
        voices=(voice,),
    )
    song = Song(
        identifier="dorian-riff",
        title="Manual Dorian Riff",
        duration=32,
        tempo_bpm=120,
        tonal_context=TonalContext(PitchClass.parse("D"), "Dorian"),
        sections=(Placement(section, 0),),
    )
    music = MusicIR(song)

    proposal = Proposal(
        identifier="proposal-001",
        intent_id=intent.identifier,
        candidate=music,
        rationale=ProposalRationale(
            summary="Repeat motif A across eight bars to establish identity.",
            objectives=(
                "remain monophonic",
                "stay within the D Dorian pitch collection",
            ),
            predicted_effects=(
                PredictedEffect("energy", delta=0.20, confidence=0.76),
            ),
        ),
    )

    critique = Critique(
        identifier="critique-001",
        critic="manual-intent-critic",
        proposal_id=proposal.identifier,
        verdict=CritiqueVerdict.SUPPORT,
        confidence=0.91,
        measurements=(Measurement("energy_delta", 0.12),),
        evidence=(
            "The motif is preserved in every bar.",
            "The voice remains monophonic.",
        ),
        reservations=(
            "The repeated rhythm increases less energy than predicted.",
        ),
    )

    decision = AcceptanceDecision(
        proposal_id=proposal.identifier,
        accepted=True,
        policy="manual-baseline-v1",
        reason="The candidate satisfies the hard-coded intent closely enough.",
        critique_ids=(critique.identifier,),
    )
    state = CompositionState().advance(proposal, decision)

    return ManualTrace(
        intent=intent,
        proposal=proposal,
        critique=critique,
        decision=decision,
        state=state,
    )
