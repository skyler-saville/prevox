# Prevox Examples

Examples are living design pressure tests. They should be small enough to read
in one sitting and musical enough to expose weaknesses in the model.

The current example is:

- `manual_trace.py` — a hand-constructed eight-bar D Dorian pipeline trace.
- `export_manual_trace_midi.py` — writes that trace to
  `artifacts/midi/manual_trace.mid` for local DAW preview.
- `export_multi_voice_midi.py` — writes a tiny lead-and-bass preview to
  `artifacts/midi/multi_voice.mid`, using renderer-local voice assignments for
  tracks, channels, velocity, and General MIDI programs.
- `export_drum_preview_midi.py` — writes a one-bar GM drum preview to
  `artifacts/midi/drum_preview.mid`, using a renderer-local drum map on MIDI
  channel 9.
- `export_theory_cohesion_midi.py` — analyzes a D Dorian lead, bass, and drum
  preview for tonal cohesion, then writes `artifacts/midi/theory_cohesion.mid`.
- `analyze_melody_hooks.py` — compares a compact repeated melody with a wider
  wandering melody using genre-neutral hook analysis metrics.

Future examples should grow toward a cookbook of musical ideas:

```text
01_drone
02_ostinato
03_pedal_tone
04_call_response
05_theme_variation
06_canon
07_rhythmic_displacement
```

Each mature example should eventually include:

- the intended musical idea;
- the Intent or direct Music IR construction;
- proposals, diagnostics, analyses, and acceptance decisions where relevant;
- canonical formatted output;
- rendered MIDI or another backend output once rendering exists.

Do not add a large example to justify a vague abstraction. Add the smallest
example that makes the architectural pressure visible.
