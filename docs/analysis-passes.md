# Analysis Passes

Analysis passes are pure read-only measurements over Music IR. They return
`AnalysisReport` values containing named metrics and optional diagnostics. They
do not mutate Music IR, repair material, generate notes, or decide whether a
proposal should be accepted.

Critics and Composers may later consume these facts.

## DensityAnalysis

Function:

```python
analyze_density(music)
```

Measures realized note activity.

Key metrics:

- `note_count`
- `duration`
- `notes_per_beat`
- `note_beats_per_beat`

Diagnostic:

- `analysis.silent_music`

## MotifReuseAnalysis

Function:

```python
analyze_motif_reuse(music)
```

Measures repeated Motif identity usage.

Key metrics:

- `motif_placement_count`
- `unique_motif_count`
- `reused_motif_count`
- `uses`

Diagnostic:

- `analysis.no_motif_reuse`

## TonalCohesionAnalysis

Function:

```python
analyze_tonal_cohesion(music)
```

Measures whether pitched voices fit the song's tonal context and whether lead
and bass form simple stable vertical intervals. Temporary drum-preview pulse
voices are ignored for tonal pitch checks.

Key metrics:

- `scale_note_count`
- `out_of_scale_note_count`
- `scale_membership_ratio`
- `vertical_interval_count`
- `stable_vertical_interval_count`

Diagnostics:

- `analysis.out_of_scale_note`
- `analysis.unsupported_tonal_context`

## MelodyHookAnalysis

Function:

```python
analyze_melody_hook(music)
```

Measures genre-neutral lead-line features associated with memorable hooks.
This is not a genre classifier and not an aesthetic verdict.

Key metrics:

- `lead_note_count`
- `unique_pitch_count`
- `pitch_repetition_ratio`
- `rhythmic_repetition_ratio`
- `range_chromas`
- `stepwise_motion_ratio`
- `large_leap_count`
- `contour_direction_changes`

Diagnostics:

- `analysis.no_lead_voice`
- `analysis.melody_too_sparse`

## Example

```bash
poetry run python examples/analyze_melody_hooks.py
```

This compares a compact repeated melody with a wider wandering melody using the
same analysis report format as the rest of the middle-end.
