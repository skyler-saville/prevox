import unittest

from fractions import Fraction

from prevox.analysis import (
    analyze_density,
    analyze_motif_reuse,
    analyze_tonal_cohesion,
)
from prevox.domain import (
    Motif,
    MusicIR,
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
from prevox.inspection import format_analysis_report


def build_reused_motif_ir() -> MusicIR:
    motif = Motif(
        "motif-a",
        duration=2,
        notes=(
            Note(Pitch.parse("D4"), offset=0, duration=1),
            Note(Pitch.parse("F4"), offset=1, duration=1),
        ),
    )
    phrase = Phrase(
        "phrase-a",
        duration=8,
        motifs=(
            Placement(motif, 0),
            Placement(motif, 4),
        ),
    )
    voice = Voice(
        "lead",
        VoiceRole.LEAD,
        phrases=(Placement(phrase, 0),),
    )
    section = Section("verse", duration=8, voices=(voice,))
    song = Song(
        "song",
        "Analysis Fixture",
        duration=8,
        tempo_bpm=120,
        tonal_context=TonalContext(PitchClass.parse("D"), "Dorian"),
        sections=(Placement(section, 0),),
    )
    return MusicIR(song)


def build_silent_ir() -> MusicIR:
    section = Section("empty", duration=4, voices=())
    song = Song(
        "silent",
        "Silent Fixture",
        duration=4,
        tempo_bpm=120,
        tonal_context=TonalContext(PitchClass.parse("D"), "Dorian"),
        sections=(Placement(section, 0),),
    )
    return MusicIR(song)


def build_tonal_cohesion_ir(*, bad_note: bool = False) -> MusicIR:
    lead_motif = Motif(
        "lead-motif",
        duration=4,
        notes=(
            Note(Pitch.parse("D4"), offset=0, duration=1),
            Note(Pitch.parse("F4"), offset=1, duration=1),
            Note(Pitch.parse("A4"), offset=2, duration=1),
            Note(Pitch.parse("C#4" if bad_note else "B4"), offset=3, duration=1),
        ),
    )
    lead_phrase = Phrase(
        "lead-phrase",
        duration=4,
        motifs=(Placement(lead_motif, 0),),
    )
    lead = Voice(
        "lead",
        VoiceRole.LEAD,
        phrases=(Placement(lead_phrase, 0),),
    )

    bass_motif = Motif(
        "bass-motif",
        duration=4,
        notes=(
            Note(Pitch.parse("D2"), offset=0, duration=1),
            Note(Pitch.parse("D2"), offset=1, duration=1),
            Note(Pitch.parse("D2"), offset=2, duration=1),
            Note(Pitch.parse("G2"), offset=3, duration=1),
        ),
    )
    bass_phrase = Phrase(
        "bass-phrase",
        duration=4,
        motifs=(Placement(bass_motif, 0),),
    )
    bass = Voice(
        "bass",
        VoiceRole.BASS,
        phrases=(Placement(bass_phrase, 0),),
    )

    drum_motif = Motif(
        "drum-motif",
        duration=4,
        notes=(
            Note(Pitch.parse("C2"), offset=0, duration=Fraction(1, 2)),
            Note(Pitch.parse("F#2"), offset=Fraction(1, 2), duration=Fraction(1, 2)),
            Note(Pitch.parse("D2"), offset=1, duration=Fraction(1, 2)),
            Note(Pitch.parse("F#2"), offset=Fraction(3, 2), duration=Fraction(1, 2)),
        ),
    )
    drum_phrase = Phrase(
        "drum-phrase",
        duration=4,
        motifs=(Placement(drum_motif, 0),),
    )
    drums = Voice(
        "drums",
        VoiceRole.PULSE,
        phrases=(Placement(drum_phrase, 0),),
    )

    section = Section("verse", duration=4, voices=(lead, bass, drums))
    song = Song(
        "cohesion",
        "Tonal Cohesion Fixture",
        duration=4,
        tempo_bpm=100,
        tonal_context=TonalContext(PitchClass.parse("D"), "Dorian"),
        sections=(Placement(section, 0),),
    )
    return MusicIR(song)


def build_unsupported_tonal_context_ir() -> MusicIR:
    motif = Motif(
        "motif",
        duration=1,
        notes=(Note(Pitch.parse("D4"), offset=0, duration=1),),
    )
    phrase = Phrase("phrase", duration=1, motifs=(Placement(motif, 0),))
    voice = Voice("lead", VoiceRole.LEAD, phrases=(Placement(phrase, 0),))
    section = Section("section", duration=1, voices=(voice,))
    song = Song(
        "unsupported",
        "Unsupported Tonal Context",
        duration=1,
        tempo_bpm=120,
        tonal_context=TonalContext(PitchClass.parse("D"), "Superlocrian"),
        sections=(Placement(section, 0),),
    )
    return MusicIR(song)


class AnalysisTests(unittest.TestCase):
    def test_density_analysis_measures_realized_notes(self) -> None:
        report = analyze_density(build_reused_motif_ir())

        metrics = {(metric.subject, metric.name): metric.value for metric in report.metrics}

        self.assertEqual(report.name, "DensityAnalysis")
        self.assertEqual(metrics[("music", "note_count")], 4)
        self.assertEqual(metrics[("music", "duration")], 8)
        self.assertEqual(metrics[("music", "notes_per_beat")], 1 / 2)
        self.assertTrue(report.diagnostics.is_success)

    def test_motif_reuse_analysis_counts_placements_by_identity(self) -> None:
        report = analyze_motif_reuse(build_reused_motif_ir())

        metrics = {(metric.subject, metric.name): metric.value for metric in report.metrics}

        self.assertEqual(metrics[("music", "motif_placement_count")], 2)
        self.assertEqual(metrics[("music", "unique_motif_count")], 1)
        self.assertEqual(metrics[("music", "reused_motif_count")], 1)
        self.assertEqual(metrics[("motif 'motif-a'", "uses")], 2)
        self.assertTrue(report.diagnostics.is_success)

    def test_density_analysis_reports_silent_music_without_raising(self) -> None:
        report = analyze_density(build_silent_ir())

        self.assertTrue(report.diagnostics.diagnostics)
        self.assertEqual(
            report.diagnostics.diagnostics[0].code,
            "analysis.silent_music",
        )
        self.assertFalse(report.diagnostics.has_errors)

    def test_analysis_report_has_canonical_readable_output(self) -> None:
        rendered = format_analysis_report(analyze_motif_reuse(build_reused_motif_ir()))

        self.assertTrue(rendered.startswith("Analysis: MotifReuseAnalysis"))
        self.assertIn("music: motif_placement_count=2", rendered)
        self.assertIn("motif 'motif-a': uses=2", rendered)

    def test_analysis_does_not_mutate_music_ir(self) -> None:
        music = build_reused_motif_ir()
        before = tuple(music.iter_notes())

        analyze_density(music)
        analyze_motif_reuse(music)

        self.assertEqual(tuple(music.iter_notes()), before)

    def test_tonal_cohesion_passes_d_dorian_lead_bass_and_ignores_drums(self) -> None:
        report = analyze_tonal_cohesion(build_tonal_cohesion_ir())
        metrics = {(metric.subject, metric.name): metric.value for metric in report.metrics}

        self.assertEqual(report.name, "TonalCohesionAnalysis")
        self.assertTrue(report.diagnostics.is_success)
        self.assertEqual(metrics[("music", "scale_note_count")], 8)
        self.assertEqual(metrics[("music", "out_of_scale_note_count")], 0)
        self.assertEqual(metrics[("music", "scale_membership_ratio")], 1)
        self.assertEqual(metrics[("music", "vertical_interval_count")], 4)
        self.assertEqual(metrics[("music", "stable_vertical_interval_count")], 2)

    def test_tonal_cohesion_reports_out_of_scale_notes(self) -> None:
        report = analyze_tonal_cohesion(build_tonal_cohesion_ir(bad_note=True))

        self.assertTrue(report.diagnostics.has_errors)
        self.assertEqual(
            tuple(diagnostic.code for diagnostic in report.diagnostics.diagnostics),
            ("analysis.out_of_scale_note",),
        )
        self.assertIn("C#4", report.diagnostics.diagnostics[0].message)

    def test_tonal_cohesion_reports_unsupported_context(self) -> None:
        report = analyze_tonal_cohesion(build_unsupported_tonal_context_ir())

        self.assertTrue(report.diagnostics.has_errors)
        self.assertEqual(
            report.diagnostics.diagnostics[0].code,
            "analysis.unsupported_tonal_context",
        )

    def test_tonal_cohesion_does_not_mutate_music_ir(self) -> None:
        music = build_tonal_cohesion_ir()
        before = tuple(music.iter_notes())

        analyze_tonal_cohesion(music)

        self.assertEqual(tuple(music.iter_notes()), before)


if __name__ == "__main__":
    unittest.main()
