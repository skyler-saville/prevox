from dataclasses import FrozenInstanceError
from fractions import Fraction
import unittest

from prevox.domain import Intent, IntentTarget, RhetoricalRole


class IntentTests(unittest.TestCase):
    def test_intent_is_immutable_and_uses_exact_duration(self) -> None:
        intent = Intent(
            identifier="question",
            role=RhetoricalRole.QUESTION,
            duration=Fraction(3, 2),
            targets=(IntentTarget("energy", 0.4),),
        )

        self.assertEqual(intent.duration, Fraction(3, 2))
        self.assertEqual(intent.target("energy"), 0.4)
        self.assertIsNone(intent.target("density"))
        with self.assertRaises(FrozenInstanceError):
            intent.duration = Fraction(2)  # type: ignore[misc]

    def test_intent_rejects_duplicate_targets(self) -> None:
        with self.assertRaisesRegex(ValueError, "unique"):
            Intent(
                identifier="duplicate-target",
                role=RhetoricalRole.ANSWER,
                duration=4,
                targets=(
                    IntentTarget("energy", 0.4),
                    IntentTarget("energy", 0.6),
                ),
            )

    def test_intent_rejects_float_time(self) -> None:
        with self.assertRaisesRegex(TypeError, "int or Fraction"):
            Intent(
                identifier="lossy-time",
                role=RhetoricalRole.TRANSITION,
                duration=0.5,  # type: ignore[arg-type]
            )


if __name__ == "__main__":
    unittest.main()
