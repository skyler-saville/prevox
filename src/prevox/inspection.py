"""Human-readable inspection of the domain pipeline."""

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

from prevox.diagnostics import Diagnostic, DiagnosticReport
from prevox.domain import (
    AcceptanceDecision,
    CompositionState,
    Critique,
    Intent,
    Motif,
    MusicIR,
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


def _diagnostic_node(diagnostic: Diagnostic) -> _Node:
    children = []
    if diagnostic.location is not None:
        children.append(_leaf(f"Location: {diagnostic.location}"))
    children.extend(
        _leaf(f"Expected: {expected}") for expected in diagnostic.expected
    )
    children.extend(_leaf(f"Note: {note}") for note in diagnostic.notes)
    return _Node(
        f"{diagnostic.severity.value.upper()} {diagnostic.code}: "
        f"{diagnostic.message}",
        tuple(children),
    )


def format_diagnostic(diagnostic: Diagnostic) -> str:
    """Return the canonical human-readable diagnostic form."""
    return _render_node(_diagnostic_node(diagnostic))


def format_diagnostic_report(report: DiagnosticReport) -> str:
    """Return the canonical human-readable diagnostic report form."""
    if not report.diagnostics:
        return "Diagnostics: clean"
    return "\n\n".join(
        _render_node(_diagnostic_node(diagnostic))
        for diagnostic in report.diagnostics
    )


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


def format_intent(intent: Intent) -> str:
    """Return the canonical human-readable Intent form."""
    return _render_node(_intent_node(intent))


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


def format_proposal(proposal: Proposal) -> str:
    """Return the canonical human-readable Proposal form."""
    return _render_node(_proposal_node(proposal))


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


def format_critique(critique: Critique) -> str:
    """Return the canonical human-readable Critique form."""
    return _render_node(_critique_node(critique))


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


def format_decision(
    decision: AcceptanceDecision,
    state: CompositionState,
) -> str:
    """Return the canonical human-readable acceptance form."""
    return _render_node(_decision_node(decision, state))


def _motif_node(motif: Motif, *, label: str | None = None) -> _Node:
    return _Node(
        label or f"Motif: {motif.identifier}",
        (
            _leaf(f"Duration: {_beat(motif.duration)} beats"),
            *(
                _leaf(
                    f"Note: {note.pitch} @ +{_beat(note.offset)} "
                    f"for {_beat(note.duration)}"
                )
                for note in motif.notes
            ),
        ),
    )


def format_motif(motif: Motif) -> str:
    """Return the canonical human-readable Motif form."""
    return _render_node(_motif_node(motif))


def _music_node(music: MusicIR) -> _Node:
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
                    motif_nodes.append(
                        _motif_node(
                            motif,
                            label=(
                                f"Motif: {motif.identifier} "
                                f"@ +{_beat(motif_placement.offset)}"
                            ),
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


def format_music_ir(music: MusicIR) -> str:
    """Return the canonical human-readable Music IR form."""
    return _render_node(_music_node(music))


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
        _music_node(proposal.candidate),
    )
    return "\n\n".join(_render_node(node) for node in nodes)
