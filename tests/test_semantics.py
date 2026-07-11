from fractions import Fraction
import unittest

from prevox.domain import Motif, Note, Pitch
from prevox.transforms import augment, diminish, reverse


def contour_motif() -> Motif:
    return Motif(
        "contour",
        duration=8,
        notes=(
            Note(Pitch.parse("D4"), offset=0, duration=1),
            Note(Pitch.parse("F4"), offset=2, duration=Fraction(1, 2)),
            Note(Pitch.parse("A4"), offset=5, duration=2),
        ),
    )


def normalized_timing(
    motif: Motif,
) -> tuple[tuple[str, Fraction, Fraction], ...]:
    return tuple(
        (
            str(note.pitch),
            note.offset / motif.duration,
            note.duration / motif.duration,
        )
        for note in sorted(motif.notes, key=lambda note: note.offset)
    )


def pitch_order_by_time(motif: Motif) -> tuple[str, ...]:
    return tuple(
        str(note.pitch)
        for note in sorted(motif.notes, key=lambda note: note.offset)
    )


class SemanticTransformationTests(unittest.TestCase):
    def test_augmentation_preserves_relative_rhythmic_shape(self) -> None:
        original = contour_motif()
        transformed = augment(original, identifier="augmented", factor=3)

        self.assertEqual(
            normalized_timing(transformed),
            normalized_timing(original),
        )

    def test_diminution_preserves_relative_rhythmic_shape(self) -> None:
        original = contour_motif()
        transformed = diminish(original, identifier="diminished", divisor=4)

        self.assertEqual(
            normalized_timing(transformed),
            normalized_timing(original),
        )

    def test_augmentation_preserves_event_order_and_pitch_sequence(self) -> None:
        original = contour_motif()
        transformed = augment(original, identifier="augmented", factor=2)

        self.assertEqual(
            pitch_order_by_time(transformed),
            pitch_order_by_time(original),
        )

    def test_reverse_preserves_durations_while_reversing_event_order(self) -> None:
        original = contour_motif()
        transformed = reverse(original, identifier="reversed")

        self.assertEqual(
            tuple(note.duration for note in transformed.notes),
            tuple(
                note.duration
                for note in sorted(
                    original.notes,
                    key=lambda note: note.offset,
                    reverse=True,
                )
            ),
        )
        self.assertEqual(
            pitch_order_by_time(transformed),
            tuple(reversed(pitch_order_by_time(original))),
        )


if __name__ == "__main__":
    unittest.main()
