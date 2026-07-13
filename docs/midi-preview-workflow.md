# MIDI Preview Workflow

Prevox currently exports Standard MIDI Files as generated preview artifacts.
These files are used to prove that backend-independent Music IR can cross into
a DAW without adding MIDI concepts to the domain.

## Commands

```bash
poetry run python examples/export_manual_trace_midi.py
poetry run python examples/export_multi_voice_midi.py
poetry run python examples/export_drum_preview_midi.py
poetry run python examples/export_theory_cohesion_midi.py
```

Generated files are written under `artifacts/midi/`:

| File | Purpose |
| --- | --- |
| `manual_trace.mid` | Single-track proof that the manual D Dorian trace renders. |
| `multi_voice.mid` | Lead and bass rendered as separate MIDI preview tracks. |
| `drum_preview.mid` | GM drum preview on MIDI channel 10. |
| `theory_cohesion.mid` | Lead, bass, and drums after tonal-cohesion analysis. |

## Artifact policy

Do not commit generated binary `.mid` files by default. They are ignored so
local DAW testing does not pollute commits.

Golden MIDI tests compare normalized textual event projections instead of raw
binary files. Binary fixtures may be added later only under an intentional
fixture policy.

## Logic proving ground

Logic is the current DAW proving ground. The recent artifacts have been imported
successfully as separate software instruments:

- lead/synth;
- bass;
- GM drums.

This validates the generic MIDI path, not a Logic-specific integration.

## Preview caveats

VS Code MIDI viewers are useful for inspecting timing, tracks, channels, and
event shape. They may not use the same sound set or General MIDI drum mapping
as Logic, so they are not authoritative for drum timbre.

If Logic renders a file correctly and a lightweight preview plugin sounds odd,
prefer Logic as the current playback authority.
