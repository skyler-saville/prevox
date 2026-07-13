from pathlib import Path
from fractions import Fraction
from io import BytesIO
import tempfile
import unittest

from mido import MidiFile, bpm2tempo

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
from prevox.export.midi import (
    MidiRenderer,
    MidiRenderProfile,
    MidiVoiceAssignment,
    midi_note_number,
)
from prevox.manual_example import build_manual_trace


GOLDEN_DIR = Path(__file__).with_name("golden")


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


def midi_projection(path: Path) -> str:
    midi = MidiFile(path)
    lines = [
        f"MidiFile type={midi.type}",
        f"Ticks per beat: {midi.ticks_per_beat}",
    ]
    for track_index, track in enumerate(midi.tracks):
        lines.append(f"Track {track_index}")
        absolute_ticks = 0
        for message in track:
            absolute_ticks += message.time
            prefix = f"  +{message.time:04d} @{absolute_ticks:05d}"
            if message.type == "track_name":
                lines.append(f"{prefix} track_name name={message.name!r}")
            elif message.type == "set_tempo":
                lines.append(f"{prefix} set_tempo tempo={message.tempo}")
            elif message.type == "program_change":
                lines.append(
                    f"{prefix} program_change program={message.program} "
                    f"channel={message.channel}"
                )
            elif message.type in {"note_on", "note_off"}:
                lines.append(
                    f"{prefix} {message.type} note={message.note} "
                    f"velocity={message.velocity} channel={message.channel}"
                )
            elif message.type == "end_of_track":
                lines.append(f"{prefix} end_of_track")
            else:
                lines.append(f"{prefix} {message}")
    return "\n".join(lines) + "\n"


def unrepresentable_music() -> MusicIR:
    motif = Motif(
        "tuplet",
        duration=1,
        notes=(Note(Pitch.parse("D4"), offset=0, duration=1),),
    )
    phrase = Phrase("phrase", duration=1, motifs=(Placement(motif, 0),))
    voice = Voice(
        "lead",
        VoiceRole.LEAD,
        phrases=(Placement(phrase, Fraction(1, 7)),),
    )
    section = Section("section", duration=2, voices=(voice,))
    song = Song(
        "song",
        "Tuplet Fixture",
        duration=2,
        tempo_bpm=120,
        tonal_context=TonalContext(PitchClass.parse("D"), "Dorian"),
        sections=(Placement(section, 0),),
    )
    return MusicIR(song)


def multi_voice_music() -> MusicIR:
    lead_motif = Motif(
        "lead-motif",
        duration=4,
        notes=(
            Note(Pitch.parse("D4"), offset=0, duration=1),
            Note(Pitch.parse("F4"), offset=1, duration=1),
            Note(Pitch.parse("A4"), offset=2, duration=2),
        ),
    )
    lead_phrase = Phrase(
        "lead-phrase",
        duration=8,
        motifs=(Placement(lead_motif, 0), Placement(lead_motif, 4)),
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
            Note(Pitch.parse("D2"), offset=0, duration=2),
            Note(Pitch.parse("A2"), offset=2, duration=2),
        ),
    )
    bass_phrase = Phrase(
        "bass-phrase",
        duration=8,
        motifs=(Placement(bass_motif, 0), Placement(bass_motif, 4)),
    )
    bass = Voice(
        "bass",
        VoiceRole.BASS,
        phrases=(Placement(bass_phrase, 0),),
    )

    section = Section("verse", duration=8, voices=(lead, bass))
    song = Song(
        "two-voice-preview",
        "Two Voice Preview",
        duration=8,
        tempo_bpm=96,
        tonal_context=TonalContext(PitchClass.parse("D"), "Dorian"),
        sections=(Placement(section, 0),),
    )
    return MusicIR(song)


def multi_voice_profile() -> MidiRenderProfile:
    return MidiRenderProfile(
        {
            "lead": MidiVoiceAssignment(
                channel=0,
                program=80,
                velocity=72,
                track_name="Lead Preview",
            ),
            "bass": MidiVoiceAssignment(
                channel=1,
                program=33,
                velocity=84,
                track_name="Bass Preview",
            ),
        }
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

    def test_manual_trace_midi_projection_matches_golden_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manual_trace.mid"

            MidiRenderer().write(manual_music(), path)

            golden = (GOLDEN_DIR / "manual_trace_midi.txt").read_text()
            self.assertEqual(midi_projection(path), golden)

    def test_rejects_invalid_renderer_parameters(self) -> None:
        with self.assertRaisesRegex(ValueError, "ticks_per_beat"):
            MidiRenderer(ticks_per_beat=0)
        with self.assertRaisesRegex(ValueError, "preview_velocity"):
            MidiRenderer(preview_velocity=0)
        with self.assertRaisesRegex(ValueError, "preview_velocity"):
            MidiRenderer(preview_velocity=128)
        with self.assertRaisesRegex(ValueError, "channel"):
            MidiRenderer(channel=-1)
        with self.assertRaisesRegex(ValueError, "channel"):
            MidiRenderer(channel=16)

    def test_rejects_pitch_outside_midi_note_range(self) -> None:
        with self.assertRaisesRegex(ValueError, "outside MIDI note range"):
            midi_note_number(Pitch.parse("B-4"))
        with self.assertRaisesRegex(ValueError, "outside MIDI note range"):
            midi_note_number(Pitch.parse("G#9"))

    def test_rejects_time_not_representable_by_ticks_per_beat(self) -> None:
        with self.assertRaisesRegex(ValueError, "not representable"):
            MidiRenderer(ticks_per_beat=480).to_midi_file(
                unrepresentable_music()
            )

    def test_write_supports_binary_file_like_object(self) -> None:
        buffer = BytesIO()

        MidiRenderer().write(manual_music(), buffer)

        buffer.seek(0)
        midi = MidiFile(file=buffer)
        self.assertEqual(midi.ticks_per_beat, 480)
        self.assertEqual(len(midi.tracks), 1)

    def test_profiled_export_creates_one_track_per_voice_plus_tempo(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "multi_voice.mid"

            MidiRenderer(profile=multi_voice_profile()).write(multi_voice_music(), path)

            midi = MidiFile(path)
            self.assertEqual(len(midi.tracks), 3)
            track_names = [
                message.name
                for track in midi.tracks
                for message in track
                if message.type == "track_name"
            ]
            self.assertEqual(
                track_names,
                [
                    "Two Voice Preview Tempo",
                    "Lead Preview",
                    "Bass Preview",
                ],
            )

    def test_profiled_export_uses_voice_assignments(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "multi_voice.mid"

            MidiRenderer(profile=multi_voice_profile()).write(multi_voice_music(), path)

            midi = MidiFile(path)
            lead_messages = tuple(
                message
                for message in midi.tracks[1]
                if message.type in {"program_change", "note_on"}
            )
            bass_messages = tuple(
                message
                for message in midi.tracks[2]
                if message.type in {"program_change", "note_on"}
            )
            self.assertEqual(lead_messages[0].program, 80)
            self.assertEqual(lead_messages[0].channel, 0)
            self.assertEqual(
                {
                    message.velocity
                    for message in lead_messages
                    if message.type == "note_on"
                },
                {72},
            )
            self.assertEqual(bass_messages[0].program, 33)
            self.assertEqual(bass_messages[0].channel, 1)
            self.assertEqual(
                {
                    message.velocity
                    for message in bass_messages
                    if message.type == "note_on"
                },
                {84},
            )

    def test_profiled_export_midi_projection_matches_golden_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "multi_voice.mid"

            MidiRenderer(profile=multi_voice_profile()).write(multi_voice_music(), path)

            golden = (GOLDEN_DIR / "multi_voice_midi.txt").read_text()
            self.assertEqual(midi_projection(path), golden)

    def test_profile_validation_rejects_invalid_voice_assignments(self) -> None:
        with self.assertRaisesRegex(ValueError, "channel"):
            MidiVoiceAssignment(channel=16)
        with self.assertRaisesRegex(ValueError, "program"):
            MidiVoiceAssignment(channel=0, program=128)
        with self.assertRaisesRegex(ValueError, "velocity"):
            MidiVoiceAssignment(channel=0, velocity=0)
        with self.assertRaisesRegex(ValueError, "track_name"):
            MidiVoiceAssignment(channel=0, track_name=" ")
        with self.assertRaisesRegex(ValueError, "voice_assignments"):
            MidiRenderProfile({})


if __name__ == "__main__":
    unittest.main()
