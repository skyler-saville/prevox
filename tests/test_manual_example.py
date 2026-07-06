import unittest

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


if __name__ == "__main__":
    unittest.main()
