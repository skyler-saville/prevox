from pathlib import Path
import unittest

from prevox.inspection import format_music_ir
from prevox.manual_example import build_manual_trace


class ManualExampleTests(unittest.TestCase):
    def test_manual_trace_is_eight_bars_of_monophonic_d_dorian(self) -> None:
        trace = build_manual_trace()
        music = trace.proposal.candidate
        notes = tuple(music.iter_notes())

        self.assertEqual(music.song.duration, 32)
        self.assertEqual(str(music.song.tonal_context), "D Dorian")
        self.assertEqual(len(notes), 32)
        self.assertEqual({str(note.pitch) for note in notes}, {"D4", "F4", "G4", "A4"})
        self.assertTrue(trace.decision.accepted)
        self.assertEqual(trace.state.revision, 1)

    def test_console_trace_exposes_the_complete_manual_pipeline(self) -> None:
        rendered = build_manual_trace().format()

        self.assertIn("Intent: dorian-escalation", rendered)
        self.assertIn("Proposal: proposal-001", rendered)
        self.assertIn("Critique: critique-001", rendered)
        self.assertIn("Decision: accepted", rendered)
        self.assertIn("MusicIR v0.1", rendered)
        self.assertIn("Motif: motif-a @ +28", rendered)
        self.assertNotIn("MIDI", rendered)

    def test_console_trace_matches_the_canonical_golden_file(self) -> None:
        golden = (
            Path(__file__).with_name("golden") / "manual_trace.txt"
        ).read_text(encoding="utf-8")

        self.assertEqual(build_manual_trace().format() + "\n", golden)

    def test_music_ir_formatter_is_stable_and_standalone(self) -> None:
        music = build_manual_trace().proposal.candidate

        first = format_music_ir(music)
        second = format_music_ir(music)

        self.assertEqual(first, second)
        self.assertTrue(first.startswith("MusicIR v0.1"))
        self.assertIn("Voice: lead (lead)", first)


if __name__ == "__main__":
    unittest.main()
