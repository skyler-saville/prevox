from fractions import Fraction
import unittest

from prevox.domain import (
    MusicIR,
    Motif,
    Note,
    Phrase,
    Pitch,
    PitchClass,
    Placement,
    Section,
    Song,
    TonalContext,
    Voice,
    VoiceRole,
)


def build_ir(
    *,
    notes: tuple[Note, ...],
    motif_offset: Fraction | int = 1,
    phrase_offset: Fraction | int = 2,
    section_offset: Fraction | int = 4,
    max_polyphony: int = 1,
) -> MusicIR:
    motif = Motif("motif", duration=4, notes=notes)
    phrase = Phrase(
        "phrase",
        duration=8,
        motifs=(Placement(motif, motif_offset),),
    )
    voice = Voice(
        "lead",
        VoiceRole.LEAD,
        phrases=(Placement(phrase, phrase_offset),),
        max_polyphony=max_polyphony,
    )
    section = Section("verse", duration=16, voices=(voice,))
    song = Song(
        "song",
        "Relative Time",
        duration=32,
        tempo_bpm=120,
        tonal_context=TonalContext(PitchClass.parse("D"), "Dorian"),
        sections=(Placement(section, section_offset),),
    )
    return MusicIR(song)


class MusicIRTests(unittest.TestCase):
    def test_local_offsets_compose_into_derived_song_time(self) -> None:
        music = build_ir(
            notes=(
                Note(
                    Pitch.parse("D4"),
                    offset=Fraction(1, 2),
                    duration=Fraction(1, 2),
                ),
            )
        )

        realized = tuple(music.iter_notes())

        self.assertEqual(len(realized), 1)
        self.assertEqual(realized[0].offset, Fraction(15, 2))
        self.assertEqual(realized[0].pitch, Pitch.parse("D4"))

    def test_child_must_fit_parent_duration(self) -> None:
        motif = Motif(
            "too-long",
            duration=4,
            notes=(Note(Pitch.parse("D4"), offset=3, duration=1),),
        )

        with self.assertRaisesRegex(ValueError, "beyond duration"):
            Phrase(
                "phrase",
                duration=4,
                motifs=(Placement(motif, 1),),
            )

    def test_monophonic_voice_rejects_overlapping_notes(self) -> None:
        notes = (
            Note(Pitch.parse("D4"), offset=0, duration=2),
            Note(Pitch.parse("F4"), offset=1, duration=2),
        )

        with self.assertRaisesRegex(ValueError, "max_polyphony"):
            build_ir(notes=notes)

    def test_polyphonic_voice_allows_declared_overlap(self) -> None:
        notes = (
            Note(Pitch.parse("D4"), offset=0, duration=2),
            Note(Pitch.parse("F4"), offset=1, duration=2),
        )

        music = build_ir(notes=notes, max_polyphony=2)

        self.assertEqual(len(tuple(music.iter_notes())), 2)

    def test_music_ir_has_no_instrument_assignment(self) -> None:
        music = build_ir(
            notes=(Note(Pitch.parse("D4"), offset=0, duration=1),)
        )
        voice = music.song.sections[0].item.voices[0]

        self.assertFalse(hasattr(voice, "instrument"))
        self.assertFalse(hasattr(voice, "midi_channel"))


if __name__ == "__main__":
    unittest.main()
