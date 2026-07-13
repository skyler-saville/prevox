"""Pure read-only analyses over Music IR."""

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

from prevox.diagnostics import (
    Diagnostic,
    DiagnosticLocation,
    DiagnosticReport,
    DiagnosticSeverity,
)
from prevox.domain._values import require_identifier
from prevox.domain.music import MusicIR, Pitch, RealizedNote, VoiceRole
from prevox.theory import (
    all_preview_percussion,
    build_scale,
    is_stable_vertical_interval,
)


MetricValue = int | Fraction | str


@dataclass(frozen=True, slots=True)
class AnalysisMetric:
    """A named fact produced by a read-only analysis pass."""

    name: str
    value: MetricValue
    subject: str = "music"
    unit: str = ""

    def __post_init__(self) -> None:
        require_identifier(self.name, field="analysis metric name")
        require_identifier(self.subject, field="analysis metric subject")
        if not isinstance(self.value, (int, Fraction, str)) or isinstance(
            self.value,
            bool,
        ):
            raise TypeError("analysis metric value must be int, Fraction, or str")
        if isinstance(self.value, str):
            require_identifier(self.value, field="analysis metric value")
        if not isinstance(self.unit, str):
            raise TypeError("analysis metric unit must be a string")


@dataclass(frozen=True, slots=True)
class AnalysisReport:
    """The immutable result of one analysis pass."""

    name: str
    metrics: tuple[AnalysisMetric, ...] = ()
    diagnostics: DiagnosticReport = DiagnosticReport()

    def __init__(
        self,
        name: str,
        metrics: Iterable[AnalysisMetric] = (),
        diagnostics: DiagnosticReport | None = None,
    ) -> None:
        object.__setattr__(
            self,
            "name",
            require_identifier(name, field="analysis report name"),
        )
        normalized_metrics = tuple(metrics)
        if any(not isinstance(metric, AnalysisMetric) for metric in normalized_metrics):
            raise TypeError("analysis report metrics must be AnalysisMetric values")
        object.__setattr__(self, "metrics", normalized_metrics)
        report = diagnostics or DiagnosticReport()
        if not isinstance(report, DiagnosticReport):
            raise TypeError("analysis diagnostics must be a DiagnosticReport")
        object.__setattr__(self, "diagnostics", report)


def _music_location(music: MusicIR) -> DiagnosticLocation:
    return DiagnosticLocation((f"Song {music.song.identifier!r}",))


def _require_music_ir(music: MusicIR) -> None:
    if not isinstance(music, MusicIR):
        raise TypeError("analysis requires a MusicIR value")


def analyze_density(music: MusicIR) -> AnalysisReport:
    """Measure realized-note density without mutating Music IR."""
    _require_music_ir(music)
    notes = tuple(music.iter_notes())
    note_count = len(notes)
    total_note_beats = sum(
        (note.duration for note in notes),
        start=Fraction(0, 1),
    )
    notes_per_beat = Fraction(note_count, 1) / music.song.duration
    note_beats_per_beat = total_note_beats / music.song.duration

    metrics = [
        AnalysisMetric("note_count", note_count),
        AnalysisMetric("duration", music.song.duration, unit="beats"),
        AnalysisMetric("notes_per_beat", notes_per_beat),
        AnalysisMetric("note_beats_per_beat", note_beats_per_beat),
    ]

    by_voice: dict[str, list[Fraction]] = {}
    for note in notes:
        by_voice.setdefault(note.voice_id, []).append(note.duration)
    for voice_id in sorted(by_voice):
        voice_durations = by_voice[voice_id]
        voice_note_count = len(voice_durations)
        metrics.extend(
            (
                AnalysisMetric(
                    "note_count",
                    voice_note_count,
                    subject=f"voice {voice_id!r}",
                ),
                AnalysisMetric(
                    "notes_per_beat",
                    Fraction(voice_note_count, 1) / music.song.duration,
                    subject=f"voice {voice_id!r}",
                ),
            )
        )

    diagnostics = DiagnosticReport()
    if note_count == 0:
        diagnostics = diagnostics.add(
            Diagnostic(
                code="analysis.silent_music",
                severity=DiagnosticSeverity.WARNING,
                message="music contains no realized notes",
                location=_music_location(music),
                expected=("at least one realized note for audible output",),
            )
        )

    return AnalysisReport("DensityAnalysis", metrics, diagnostics)


def analyze_motif_reuse(music: MusicIR) -> AnalysisReport:
    """Measure how often Motif identities are reused across the Music IR."""
    _require_music_ir(music)
    motif_counts: dict[str, int] = {}
    for section_placement in music.song.sections:
        section = section_placement.item
        for voice in section.voices:
            for phrase_placement in voice.phrases:
                phrase = phrase_placement.item
                for motif_placement in phrase.motifs:
                    motif_id = motif_placement.item.identifier
                    motif_counts[motif_id] = motif_counts.get(motif_id, 0) + 1

    placement_count = sum(motif_counts.values())
    reused_count = sum(1 for count in motif_counts.values() if count > 1)
    metrics = [
        AnalysisMetric("motif_placement_count", placement_count),
        AnalysisMetric("unique_motif_count", len(motif_counts)),
        AnalysisMetric("reused_motif_count", reused_count),
        *(
            AnalysisMetric(
                "uses",
                motif_counts[motif_id],
                subject=f"motif {motif_id!r}",
            )
            for motif_id in sorted(motif_counts)
        ),
    ]

    diagnostics = DiagnosticReport()
    if placement_count > 1 and reused_count == 0:
        diagnostics = diagnostics.add(
            Diagnostic(
                code="analysis.no_motif_reuse",
                severity=DiagnosticSeverity.INFO,
                message="no motif identity is reused",
                location=_music_location(music),
                notes=("motif reuse is optional, but useful for thematic coherence",),
            )
        )

    return AnalysisReport("MotifReuseAnalysis", metrics, diagnostics)


def analyze_tonal_cohesion(music: MusicIR) -> AnalysisReport:
    """Measure basic scale and lead/bass interval cohesion for Music IR."""
    _require_music_ir(music)
    diagnostics = DiagnosticReport()
    try:
        scale = build_scale(music.song.tonal_context)
    except ValueError:
        diagnostics = diagnostics.add(
            Diagnostic(
                code="analysis.unsupported_tonal_context",
                severity=DiagnosticSeverity.ERROR,
                message="tonal context is not supported by tonal cohesion analysis",
                location=_music_location(music),
                expected=("one of the supported common seven-note modes",),
                notes=(f"received {music.song.tonal_context}",),
            )
        )
        return AnalysisReport("TonalCohesionAnalysis", diagnostics=diagnostics)

    notes = tuple(music.iter_notes())
    ignored_voice_ids = _preview_percussion_voice_ids(music)
    tonal_notes = tuple(
        note for note in notes if note.voice_id not in ignored_voice_ids
    )
    scale_notes = tuple(note for note in tonal_notes if scale.contains(note.pitch))
    out_of_scale_notes = tuple(
        note for note in tonal_notes if not scale.contains(note.pitch)
    )

    for note in out_of_scale_notes:
        diagnostics = diagnostics.add(
            Diagnostic(
                code="analysis.out_of_scale_note",
                severity=DiagnosticSeverity.ERROR,
                message=f"note {note.pitch} is outside {music.song.tonal_context}",
                location=DiagnosticLocation(
                    (
                        f"Song {music.song.identifier!r}",
                        f"Section {note.section_id!r}",
                        f"Voice {note.voice_id!r}",
                        f"Phrase {note.phrase_id!r}",
                        f"Motif {note.motif_id!r}",
                    )
                ),
                expected=(f"pitch class in {music.song.tonal_context}",),
            )
        )

    vertical_intervals = _lead_bass_vertical_intervals(music, tonal_notes)
    stable_vertical_intervals = tuple(
        interval for interval in vertical_intervals if interval[2]
    )
    tonal_note_count = len(tonal_notes)
    metrics = [
        AnalysisMetric("scale_note_count", len(scale_notes)),
        AnalysisMetric("out_of_scale_note_count", len(out_of_scale_notes)),
        AnalysisMetric(
            "scale_membership_ratio",
            Fraction(len(scale_notes), tonal_note_count)
            if tonal_note_count
            else Fraction(0, 1),
        ),
        AnalysisMetric("vertical_interval_count", len(vertical_intervals)),
        AnalysisMetric(
            "stable_vertical_interval_count",
            len(stable_vertical_intervals),
        ),
    ]
    return AnalysisReport("TonalCohesionAnalysis", metrics, diagnostics)


def _preview_percussion_voice_ids(music: MusicIR) -> set[str]:
    voice_roles = {
        voice.identifier: voice.role
        for section_placement in music.song.sections
        for voice in section_placement.item.voices
    }
    notes_by_voice: dict[str, list[Pitch]] = {}
    for note in music.iter_notes():
        notes_by_voice.setdefault(note.voice_id, []).append(note.pitch)
    return {
        voice_id
        for voice_id, pitches in notes_by_voice.items()
        if voice_roles.get(voice_id) is VoiceRole.PULSE
        and all_preview_percussion(pitches)
    }


def _lead_bass_vertical_intervals(
    music: MusicIR,
    notes: Iterable[RealizedNote],
) -> tuple[tuple[RealizedNote, RealizedNote, bool], ...]:
    voice_roles = {
        voice.identifier: voice.role
        for section_placement in music.song.sections
        for voice in section_placement.item.voices
    }
    lead_by_offset = {
        note.offset: note
        for note in notes
        if voice_roles.get(note.voice_id) is VoiceRole.LEAD
    }
    bass_by_offset = {
        note.offset: note
        for note in notes
        if voice_roles.get(note.voice_id) is VoiceRole.BASS
    }
    intervals = []
    for offset in sorted(set(lead_by_offset).intersection(bass_by_offset)):
        lead = lead_by_offset[offset]
        bass = bass_by_offset[offset]
        intervals.append(
            (
                bass,
                lead,
                is_stable_vertical_interval(bass.pitch, lead.pitch),
            )
        )
    return tuple(intervals)
