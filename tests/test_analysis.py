import unittest

from prevox.analysis import analyze_density, analyze_motif_reuse
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


if __name__ == "__main__":
    unittest.main()
