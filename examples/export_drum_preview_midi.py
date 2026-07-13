"""Export a General MIDI drum preview using a backend-local drum map."""

from fractions import Fraction
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


def build_drum_preview() -> MusicIR:
    """Build a tiny rhythm voice with no MIDI drum concepts in Music IR."""
    motif = Motif(
        "drum-motif",
        duration=4,
        notes=(
            Note(Pitch.parse("C2"), offset=0, duration=Fraction(1, 2)),
            Note(Pitch.parse("F#2"), offset=Fraction(1, 2), duration=Fraction(1, 2)),
            Note(Pitch.parse("D2"), offset=1, duration=Fraction(1, 2)),
            Note(Pitch.parse("F#2"), offset=Fraction(3, 2), duration=Fraction(1, 2)),
            Note(Pitch.parse("C2"), offset=2, duration=Fraction(1, 2)),
            Note(Pitch.parse("F#2"), offset=Fraction(5, 2), duration=Fraction(1, 2)),
            Note(Pitch.parse("D2"), offset=3, duration=Fraction(1, 2)),
            Note(Pitch.parse("G#2"), offset=Fraction(7, 2), duration=Fraction(1, 2)),
        ),
    )
    phrase = Phrase("drum-phrase", duration=4, motifs=(Placement(motif, 0),))
    drums = Voice(
        "drums",
        VoiceRole.PULSE,
        phrases=(Placement(phrase, 0),),
    )
    section = Section("groove", duration=4, voices=(drums,))
    song = Song(
        "drum-preview",
        "Drum Preview",
        duration=4,
        tempo_bpm=100,
        tonal_context=TonalContext(PitchClass.parse("D"), "Dorian"),
        sections=(Placement(section, 0),),
    )
    return MusicIR(song)


def drum_profile() -> MidiRenderProfile:
    """Map the pulse voice to General MIDI drums on channel 9."""
    return MidiRenderProfile(
        {
            "drums": MidiVoiceAssignment.gm_drums(
                velocity=96,
                track_name="GM Drum Preview",
            ),
        }
    )


def main() -> None:
    target = Path("artifacts/midi/drum_preview.mid")
    MidiRenderer(profile=drum_profile()).write(build_drum_preview(), target)
    print(f"Wrote {target}")


if __name__ == "__main__":
    main()
