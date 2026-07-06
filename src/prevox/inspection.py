"""Human-readable inspection of the domain pipeline."""

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

from prevox.domain import (
    AcceptanceDecision,
    CompositionState,
    Critique,
    Intent,
    Proposal,
)


@dataclass(frozen=True, slots=True)
class _Node:
    label: str
    children: tuple["_Node", ...] = ()


def _beat(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _signed(value: float) -> str:
    return f"{value:+.2f}"


def _leaf(label: str) -> _Node:
    return _Node(label)


def _render_node(node: _Node) -> str:
    lines = [node.label]

    def append_children(
        parent: _Node,
        *,
        prefix: str,
    ) -> None:
        for index, child in enumerate(parent.children):
            is_last = index == len(parent.children) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{child.label}")
            child_prefix = f"{prefix}{'    ' if is_last else '│   '}"
            append_children(child, prefix=child_prefix)

    append_children(node, prefix="")
    return "\n".join(lines)


def _intent_node(intent: Intent) -> _Node:
    children = [
        _leaf(f"Role: {intent.role.value}"),
        _leaf(f"Duration: {_beat(intent.duration)} beats"),
        *(
            _leaf(f"Target: {target.name}={target.value:.2f}")
            for target in intent.targets
        ),
        *(
            _leaf(f"Preserve: {preserved}")
            for preserved in intent.preserve
        ),
    ]
    return _Node(f"Intent: {intent.identifier}", tuple(children))


def _proposal_node(proposal: Proposal) -> _Node:
    children = [
        _leaf(f"Intent: {proposal.intent_id}"),
        _leaf(f"Reason: {proposal.rationale.summary}"),
        *(
            _leaf(f"Objective: {objective}")
            for objective in proposal.rationale.objectives
        ),
        *(
            _leaf(
                f"Predicted: {effect.name} {_signed(effect.delta)} "
                f"(confidence {effect.confidence:.2f})"
            )
            for effect in proposal.rationale.predicted_effects
        ),
    ]
    return _Node(f"Proposal: {proposal.identifier}", tuple(children))


def _critique_node(critique: Critique) -> _Node:
    children = [
        _leaf(f"Critic: {critique.critic}"),
        _leaf(f"Verdict: {critique.verdict.value}"),
        _leaf(f"Confidence: {critique.confidence:.2f}"),
        *(
            _leaf(f"Measured: {measurement.name}={measurement.value:.2f}")
            for measurement in critique.measurements
        ),
        *(_leaf(f"Evidence: {item}") for item in critique.evidence),
        *(
            _leaf(f"Reservation: {item}")
            for item in critique.reservations
        ),
    ]
    return _Node(f"Critique: {critique.identifier}", tuple(children))


def _decision_node(
    decision: AcceptanceDecision,
    state: CompositionState,
) -> _Node:
    return _Node(
        f"Decision: {'accepted' if decision.accepted else 'rejected'}",
        (
            _leaf(f"Policy: {decision.policy}"),
            _leaf(f"Reason: {decision.reason}"),
            _leaf(f"State revision: {state.revision}"),
        ),
    )


def _music_node(proposal: Proposal) -> _Node:
    music = proposal.candidate
    song = music.song
    section_nodes = []
    for section_placement in song.sections:
        section = section_placement.item
        voice_nodes = []
        for voice in section.voices:
            phrase_nodes = []
            for phrase_placement in voice.phrases:
                phrase = phrase_placement.item
                motif_nodes = []
                for motif_placement in phrase.motifs:
                    motif = motif_placement.item
                    note_nodes = tuple(
                        _leaf(
                            f"Note: {note.pitch} @ +{_beat(note.offset)} "
                            f"for {_beat(note.duration)}"
                        )
                        for note in motif.notes
                    )
                    motif_nodes.append(
                        _Node(
                            f"Motif: {motif.identifier} "
                            f"@ +{_beat(motif_placement.offset)}",
                            note_nodes,
                        )
                    )
                phrase_nodes.append(
                    _Node(
                        f"Phrase: {phrase.identifier} "
                        f"@ +{_beat(phrase_placement.offset)}",
                        tuple(motif_nodes),
                    )
                )
            voice_nodes.append(
                _Node(
                    f"Voice: {voice.identifier} ({voice.role.value})",
                    tuple(phrase_nodes),
                )
            )
        section_nodes.append(
            _Node(
                f"Section: {section.identifier} "
                f"@ +{_beat(section_placement.offset)}",
                tuple(voice_nodes),
            )
        )

    return _Node(
        f"MusicIR v{music.schema_version}",
        (
            _Node(
                f"Song: {song.title}",
                (
                    _leaf(f"Tonal context: {song.tonal_context}"),
                    _leaf(f"Tempo: {song.tempo_bpm} BPM"),
                    _leaf(f"Duration: {_beat(song.duration)} beats"),
                    *section_nodes,
                ),
            ),
        ),
    )


def format_trace(
    *,
    intent: Intent,
    proposal: Proposal,
    critiques: Iterable[Critique],
    decision: AcceptanceDecision,
    state: CompositionState,
) -> str:
    """Render an inspectable trace without exposing object repr internals."""
    nodes = (
        _intent_node(intent),
        _proposal_node(proposal),
        *(_critique_node(critique) for critique in critiques),
        _decision_node(decision, state),
        _music_node(proposal),
    )
    return "\n\n".join(_render_node(node) for node in nodes)
