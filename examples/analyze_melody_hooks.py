"""Compare two genre-neutral melody hook analysis reports."""

from fractions import Fraction

from prevox.analysis import analyze_melody_hook
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


def _melody_fixture(
    identifier: str,
    notes: tuple[Note, ...],
) -> MusicIR:
    motif = Motif(f"{identifier}-motif", duration=8, notes=notes)
    phrase = Phrase(
        f"{identifier}-phrase",
        duration=8,
        motifs=(Placement(motif, 0),),
    )
    lead = Voice("lead", VoiceRole.LEAD, phrases=(Placement(phrase, 0),))
    section = Section("verse", duration=8, voices=(lead,))
    song = Song(
        identifier,
        f"{identifier} Melody",
        duration=8,
        tempo_bpm=120,
        tonal_context=TonalContext(PitchClass.parse("D"), "Dorian"),
        sections=(Placement(section, 0),),
    )
    return MusicIR(song)


def hook_like_melody() -> MusicIR:
    """Build a compact repeated melody with simple rhythm and small range."""
    return _melody_fixture(
        "hook-like",
        (
            Note(Pitch.parse("D4"), offset=0, duration=1),
            Note(Pitch.parse("F4"), offset=1, duration=1),
            Note(Pitch.parse("G4"), offset=2, duration=1),
            Note(Pitch.parse("F4"), offset=3, duration=1),
            Note(Pitch.parse("D4"), offset=4, duration=1),
            Note(Pitch.parse("F4"), offset=5, duration=1),
            Note(Pitch.parse("G4"), offset=6, duration=1),
            Note(Pitch.parse("F4"), offset=7, duration=1),
        ),
    )


def wandering_melody() -> MusicIR:
    """Build a wider, less repetitive melody for contrast."""
    return _melody_fixture(
        "wandering",
        (
            Note(Pitch.parse("D3"), offset=0, duration=Fraction(1, 2)),
            Note(Pitch.parse("A4"), offset=Fraction(1, 2), duration=Fraction(3, 2)),
            Note(Pitch.parse("E3"), offset=2, duration=Fraction(1, 2)),
            Note(Pitch.parse("C5"), offset=Fraction(5, 2), duration=1),
            Note(Pitch.parse("F3"), offset=Fraction(7, 2), duration=Fraction(1, 2)),
            Note(Pitch.parse("B4"), offset=4, duration=2),
            Note(Pitch.parse("G3"), offset=6, duration=Fraction(1, 2)),
            Note(Pitch.parse("D5"), offset=Fraction(13, 2), duration=1),
        ),
    )


def main() -> None:
    for label, music in (
        ("Hook-like melody", hook_like_melody()),
        ("Wandering melody", wandering_melody()),
    ):
        print(label)
        print("=" * len(label))
        print(format_analysis_report(analyze_melody_hook(music)))
        print()


if __name__ == "__main__":
    main()
