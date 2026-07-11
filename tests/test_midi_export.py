from pathlib import Path
import tempfile
import unittest

from mido import MidiFile, bpm2tempo

from prevox.export.midi import MidiRenderer, midi_note_number
from prevox.domain import Pitch
from prevox.manual_example import build_manual_trace


def manual_music():
    music = build_manual_trace().state.music
    if music is None:
        raise AssertionError("manual trace should produce accepted MusicIR")
    return music


def read_messages(path: Path):
    return tuple(message for track in MidiFile(path).tracks for message in track)


def note_on_messages(path: Path):
    return tuple(
        message
        for message in read_messages(path)
        if message.type == "note_on" and message.velocity > 0
    )


class MidiExportTests(unittest.TestCase):
    def test_write_creates_readable_midi_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manual_trace.mid"

            MidiRenderer().write(manual_music(), path)

            midi = MidiFile(path)
            self.assertEqual(midi.ticks_per_beat, 480)
            self.assertEqual(len(midi.tracks), 1)

    def test_export_includes_tempo_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manual_trace.mid"

            MidiRenderer().write(manual_music(), path)

            tempo_messages = [
                message
                for message in read_messages(path)
                if message.type == "set_tempo"
            ]
            self.assertEqual(len(tempo_messages), 1)
            self.assertEqual(tempo_messages[0].tempo, bpm2tempo(120))

    def test_export_contains_expected_note_events(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manual_trace.mid"

            MidiRenderer().write(manual_music(), path)

            note_ons = note_on_messages(path)
            self.assertEqual(len(note_ons), 32)
            self.assertEqual(
                tuple(message.note for message in note_ons[:4]),
                (
                    midi_note_number(Pitch.parse("D4")),
                    midi_note_number(Pitch.parse("F4")),
                    midi_note_number(Pitch.parse("G4")),
                    midi_note_number(Pitch.parse("A4")),
                ),
            )
            self.assertEqual(
                {message.velocity for message in note_ons},
                {64},
            )

    def test_export_ordering_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manual_trace.mid"

            MidiRenderer().write(manual_music(), path)

            messages = read_messages(path)
            note_messages = [
                message for message in messages if message.type in {"note_on", "note_off"}
            ]
            self.assertEqual(note_messages[0].time, 0)
            self.assertEqual(note_messages[0].type, "note_on")
            self.assertEqual(note_messages[1].time, 480)
            self.assertEqual(note_messages[1].type, "note_off")
            self.assertEqual(note_messages[2].time, 0)
            self.assertEqual(note_messages[2].type, "note_on")

    def test_repeated_exports_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.mid"
            second = Path(directory) / "second.mid"
            renderer = MidiRenderer()
            music = manual_music()

            renderer.write(music, first)
            renderer.write(music, second)

            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_export_does_not_mutate_music_ir(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manual_trace.mid"
            music = manual_music()
            before = tuple(music.iter_notes())

            MidiRenderer().write(music, path)

            self.assertEqual(tuple(music.iter_notes()), before)

    def test_pitch_to_midi_mapping_is_backend_local_preview_policy(self) -> None:
        self.assertEqual(midi_note_number(Pitch.parse("C4")), 60)
        self.assertEqual(midi_note_number(Pitch.parse("D4")), 62)
        self.assertEqual(midi_note_number(Pitch.parse("C#4")), 61)
        self.assertEqual(midi_note_number(Pitch.parse("Db4")), 61)


if __name__ == "__main__":
    unittest.main()
