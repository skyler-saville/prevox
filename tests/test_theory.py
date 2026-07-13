import unittest

from prevox.domain import Pitch, PitchClass, TonalContext
from prevox.theory import (
    build_scale,
    is_stable_vertical_interval,
    pitch_class_chroma,
)


class TheoryTests(unittest.TestCase):
    def test_d_dorian_scale_contains_expected_pitch_classes(self) -> None:
        scale = build_scale(TonalContext(PitchClass.parse("D"), "Dorian"))

        self.assertTrue(all(scale.contains(Pitch.parse(pitch)) for pitch in (
            "D4",
            "E4",
            "F4",
            "G4",
            "A4",
            "B4",
            "C5",
        )))

    def test_d_dorian_scale_rejects_non_member_pitch_classes(self) -> None:
        scale = build_scale(TonalContext(PitchClass.parse("D"), "Dorian"))

        self.assertFalse(scale.contains(Pitch.parse("C#4")))
        self.assertFalse(scale.contains(Pitch.parse("Eb4")))

    def test_pitch_class_chroma_is_enharmonic_without_erasing_spelling(self) -> None:
        self.assertEqual(pitch_class_chroma(PitchClass.parse("C#")), 1)
        self.assertEqual(pitch_class_chroma(PitchClass.parse("Db")), 1)
        self.assertNotEqual(PitchClass.parse("C#"), PitchClass.parse("Db"))

    def test_rejects_unsupported_modes(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported tonal context mode"):
            build_scale(TonalContext(PitchClass.parse("D"), "Superlocrian"))

    def test_stable_vertical_intervals_cover_unison_octave_and_fifth(self) -> None:
        self.assertTrue(
            is_stable_vertical_interval(Pitch.parse("D2"), Pitch.parse("D4"))
        )
        self.assertTrue(
            is_stable_vertical_interval(Pitch.parse("D2"), Pitch.parse("A4"))
        )
        self.assertFalse(
            is_stable_vertical_interval(Pitch.parse("D2"), Pitch.parse("F4"))
        )


if __name__ == "__main__":
    unittest.main()
