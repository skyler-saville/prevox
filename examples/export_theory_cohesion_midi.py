"""Analyze and export a small D Dorian lead, bass, and drum preview."""

from fractions import Fraction
from pathlib import Path

from prevox.analysis import analyze_tonal_cohesion
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
from prevox.inspection import format_analysis_report


def build_theory_cohesion_preview() -> MusicIR:
    """Build a tiny D Dorian ensemble with no MIDI concepts in Music IR."""
    lead_motif = Motif(
        "lead-motif",
        duration=4,
        notes=(
            Note(Pitch.parse("D4"), offset=0, duration=1),
            Note(Pitch.parse("F4"), offset=1, duration=1),
            Note(Pitch.parse("A4"), offset=2, duration=1),
            Note(Pitch.parse("B4"), offset=3, duration=1),
        ),
    )
    lead_phrase = Phrase(
        "lead-phrase",
        duration=4,
        motifs=(Placement(lead_motif, 0),),
    )
    lead = Voice("lead", VoiceRole.LEAD, phrases=(Placement(lead_phrase, 0),))

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
    bass = Voice("bass", VoiceRole.BASS, phrases=(Placement(bass_phrase, 0),))

    drum_motif = Motif(
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
    drum_phrase = Phrase(
        "drum-phrase",
        duration=4,
        motifs=(Placement(drum_motif, 0),),
    )
    drums = Voice("drums", VoiceRole.PULSE, phrases=(Placement(drum_phrase, 0),))

    section = Section("verse", duration=4, voices=(lead, bass, drums))
    song = Song(
        "theory-cohesion-preview",
        "Theory Cohesion Preview",
        duration=4,
        tempo_bpm=100,
        tonal_context=TonalContext(PitchClass.parse("D"), "Dorian"),
        sections=(Placement(section, 0),),
    )
    return MusicIR(song)


def preview_profile() -> MidiRenderProfile:
    """Map logical voices to MIDI preview assignments in the backend."""
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
            "drums": MidiVoiceAssignment.gm_drums(
                velocity=96,
                track_name="GM Drum Preview",
            ),
        }
    )


def main() -> None:
    music = build_theory_cohesion_preview()
    print(format_analysis_report(analyze_tonal_cohesion(music)))

    target = Path("artifacts/midi/theory_cohesion.mid")
    MidiRenderer(profile=preview_profile()).write(music, target)
    print(f"\nWrote {target}")


if __name__ == "__main__":
    main()
