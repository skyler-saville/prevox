from dataclasses import FrozenInstanceError
import unittest

from prevox.domain import (
    AcceptanceDecision,
    CompositionState,
    Critique,
    CritiqueVerdict,
    Measurement,
)
from prevox.manual_example import build_manual_trace


class EvaluationTests(unittest.TestCase):
    def test_acceptance_advances_to_a_new_immutable_state(self) -> None:
        trace = build_manual_trace()
        initial = CompositionState()

        advanced = initial.advance(trace.proposal, trace.decision)

        self.assertEqual(initial.revision, 0)
        self.assertIsNone(initial.music)
        self.assertEqual(advanced.revision, 1)
        self.assertIs(advanced.music, trace.proposal.candidate)
        with self.assertRaises(FrozenInstanceError):
            advanced.revision = 2  # type: ignore[misc]

    def test_rejected_proposal_cannot_advance_state(self) -> None:
        trace = build_manual_trace()
        rejected = AcceptanceDecision(
            proposal_id=trace.proposal.identifier,
            accepted=False,
            policy="manual",
            reason="Not selected.",
        )

        with self.assertRaisesRegex(ValueError, "rejected"):
            CompositionState().advance(trace.proposal, rejected)

    def test_critique_is_independent_from_proposal_prediction(self) -> None:
        trace = build_manual_trace()
        predicted = trace.proposal.rationale.predicted_effects[0]
        measured = trace.critique.measurements[0]

        self.assertEqual(predicted.delta, 0.20)
        self.assertEqual(measured.value, 0.12)
        self.assertNotEqual(predicted.delta, measured.value)

    def test_critique_requires_normalized_confidence(self) -> None:
        with self.assertRaisesRegex(ValueError, "between"):
            Critique(
                identifier="bad-confidence",
                critic="test",
                proposal_id="proposal",
                verdict=CritiqueVerdict.ABSTAIN,
                confidence=1.1,
                measurements=(Measurement("energy", 0.1),),
            )


if __name__ == "__main__":
    unittest.main()
