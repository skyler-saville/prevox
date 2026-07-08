from fractions import Fraction
import unittest

from prevox.domain import Motif, Note, Pitch
from prevox.inspection import format_diagnostic_report, format_motif
from prevox.transforms import augment, diminish, repeat, reverse, scale_time
from prevox.transforms import (
    diagnose_diminish,
    diagnose_repeat,
    diagnose_scale_time,
)


def motif_signature(
    motif: Motif,
) -> tuple[Fraction, tuple[tuple[str, Fraction, Fraction], ...]]:
    return (
        motif.duration,
        tuple(
            (str(note.pitch), note.offset, note.duration)
            for note in motif.notes
        ),
    )


def source_motif() -> Motif:
    return Motif(
        identifier="source",
        duration=4,
        notes=(
            Note(Pitch.parse("D4"), offset=0, duration=1),
            Note(Pitch.parse("F4"), offset=1, duration=Fraction(1, 2)),
            Note(Pitch.parse("A4"), offset=3, duration=1),
        ),
    )


class MotifTransformationTests(unittest.TestCase):
    def test_reverse_reflects_notes_in_local_time(self) -> None:
        transformed = reverse(source_motif(), identifier="reversed")

        self.assertEqual(
            tuple((str(note.pitch), note.offset) for note in transformed.notes),
            (
                ("A4", Fraction(0)),
                ("F4", Fraction(5, 2)),
                ("D4", Fraction(3)),
            ),
        )

    def test_reverse_is_an_involution_over_musical_material(self) -> None:
        original = source_motif()
        reversed_once = reverse(original, identifier="reverse-1")
        reversed_twice = reverse(reversed_once, identifier="reverse-2")

        self.assertEqual(
            motif_signature(reversed_twice),
            motif_signature(original),
        )

    def test_repeat_concatenates_exact_copies(self) -> None:
        transformed = repeat(source_motif(), 3, identifier="repeated")

        self.assertEqual(transformed.duration, 12)
        self.assertEqual(len(transformed.notes), 9)
        self.assertEqual(
            tuple(note.offset for note in transformed.notes if str(note.pitch) == "D4"),
            (Fraction(0), Fraction(4), Fraction(8)),
        )

    def test_augment_then_diminish_restores_material(self) -> None:
        original = source_motif()
        augmented = augment(original, identifier="augmented")
        restored = diminish(augmented, identifier="restored")

        self.assertEqual(motif_signature(restored), motif_signature(original))

    def test_scale_time_supports_exact_tuplet_factors(self) -> None:
        transformed = scale_time(
            source_motif(),
            Fraction(2, 3),
            identifier="triplet-scale",
        )

        self.assertEqual(transformed.duration, Fraction(8, 3))
        self.assertEqual(transformed.notes[1].offset, Fraction(2, 3))
        self.assertEqual(transformed.notes[1].duration, Fraction(1, 3))

    def test_transformations_do_not_mutate_the_source(self) -> None:
        original = source_motif()
        signature = motif_signature(original)

        reverse(original, identifier="reversed")
        repeat(original, 2, identifier="repeated")
        augment(original, identifier="augmented")

        self.assertEqual(motif_signature(original), signature)
        self.assertEqual(original.identifier, "source")

    def test_transformed_motif_has_canonical_readable_output(self) -> None:
        transformed = reverse(source_motif(), identifier="reversed")

        rendered = format_motif(transformed)

        self.assertTrue(rendered.startswith("Motif: reversed"))
        self.assertIn("Duration: 4 beats", rendered)
        self.assertIn("Note: A4 @ +0 for 1", rendered)

    def test_transforms_require_explicit_exact_parameters(self) -> None:
        with self.assertRaisesRegex(TypeError, "int or Fraction"):
            scale_time(
                source_motif(),
                0.5,  # type: ignore[arg-type]
                identifier="lossy",
            )
        with self.assertRaisesRegex(ValueError, "greater than one"):
            augment(source_motif(), identifier="not-augmented", factor=1)
        with self.assertRaisesRegex(ValueError, "positive integer"):
            repeat(source_motif(), 0, identifier="empty")

    def test_transform_diagnostics_report_invalid_parameters(self) -> None:
        report = diagnose_diminish(
            source_motif(),
            identifier="too-small",
            divisor=0,
        )

        self.assertTrue(report.has_errors)
        self.assertEqual(
            report.errors[0].code,
            "transform.invalid_diminution_divisor",
        )

        rendered = format_diagnostic_report(report)
        self.assertIn(
            "ERROR transform.invalid_diminution_divisor: "
            "cannot diminish by 0",
            rendered,
        )
        self.assertIn("Location: Motif 'source'", rendered)
        self.assertIn("Expected: divisor is greater than one", rendered)

    def test_transform_diagnostics_reject_lossy_time_without_raising(self) -> None:
        report = diagnose_scale_time(
            source_motif(),
            0.5,
            identifier="lossy",
        )

        self.assertTrue(report.has_errors)
        self.assertIn(
            "floating-point factors are rejected",
            format_diagnostic_report(report),
        )

    def test_valid_transform_parameters_have_clean_diagnostics(self) -> None:
        self.assertTrue(
            diagnose_repeat(source_motif(), 2, identifier="twice").is_success
        )
        self.assertEqual(
            format_diagnostic_report(
                diagnose_repeat(source_motif(), 2, identifier="twice")
            ),
            "Diagnostics: clean",
        )


if __name__ == "__main__":
    unittest.main()
