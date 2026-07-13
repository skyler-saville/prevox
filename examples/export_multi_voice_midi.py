"""Export a two-voice MIDI preview with renderer-local voice assignments."""

from pathlib import Path

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
from prevox.export.midi import MidiRenderer, MidiRenderProfile, MidiVoiceAssignment


def build_multi_voice_preview() -> MusicIR:
    """Build a tiny lead-and-bass Music IR fixture with no MIDI concerns."""
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


def preview_profile() -> MidiRenderProfile:
    """Map logical voices to General MIDI preview programs in the backend."""
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


def main() -> None:
    target = Path("artifacts/midi/multi_voice.mid")
    MidiRenderer(profile=preview_profile()).write(build_multi_voice_preview(), target)
    print(f"Wrote {target}")


if __name__ == "__main__":
    main()
