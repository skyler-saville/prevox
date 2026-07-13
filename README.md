# Prevox

Prevox is an open-source procedural composition engine for musicians. It treats
a song as a reproducible program: Composers propose material, Critics evaluate
it, transformations develop it, and Renderers carry the result into a DAW. The
musician remains the author.

Prevox uses two backend-independent semantic levels:

```text
Intent IR → Composer → Proposal → Critics/Arbiter
                                      ↓ accepted
                         CompositionState + Music IR
                                      ↓
                                  Renderer
```

Intent IR describes what the composition is trying to do. Music IR describes
the musical structure that realizes it. Prevox composes music rather than audio.

Its first proving loop is deliberately small:

```python
plan = CompositionPlan(key="D Dorian", bars=8)
plan.add(PhraseIntent(role="question"))
plan.add(PhraseIntent(role="answer"))

music = compose(plan, seed=48291)
MidiRenderer(profile="gm-preview").write(music, "test.mid")
```

If `test.mid` opens in a DAW and plays the same eight bars when regenerated from
the same seed, the foundation works.

## Project documents

- [LLM_CONTEXT.md](LLM_CONTEXT.md) is the living project status and handoff
  document for future LLM sessions.
- [PHILOSOPHY.md](PHILOSOPHY.md) records the beliefs used to resolve product
  and design tradeoffs.
- [VISION.md](VISION.md) explains why Prevox exists and what it will not become.
- [ARCHITECTURE.md](ARCHITECTURE.md) defines boundaries, dependencies, and the
  composition pipeline.
- [MUSICAL_GRAMMAR.md](MUSICAL_GRAMMAR.md) establishes the shared musical
  vocabulary and semantics of both IRs.
- [ROADMAP.md](ROADMAP.md) turns the vision into small, testable milestones.
- [docs/capabilities.md](docs/capabilities.md) tracks what the current IR and
  compiler stages support.
- [REFERENCES.md](REFERENCES.md) is the project's annotated research notebook.
- [CONTRIBUTING.md](CONTRIBUTING.md) defines the engineering guardrails for
  protecting the architecture.
- [docs/adr/](docs/adr/) records accepted architectural decisions and their
  consequences.
- [examples/](examples/) is the start of a cookbook of small musical pressure
  tests.

## Run the architecture trace

Prevox currently implements immutable core types and one completely manual
eight-bar D Dorian trace. The first deterministic middle-end transformations
support reversing, repeating, augmenting, and diminishing Motifs. It
deliberately contains no Composer, randomness, MIDI import, or full rendering
profile yet. A minimal MIDI file exporter exists for previewing the manual
trace.

```bash
poetry install
poetry run python -m unittest discover -s tests -v
poetry run python examples/manual_trace.py
poetry run python examples/export_manual_trace_midi.py
poetry run python examples/export_multi_voice_midi.py
poetry run python examples/export_drum_preview_midi.py
poetry run python examples/export_theory_cohesion_midi.py
poetry run python examples/analyze_melody_hooks.py
```

The tests include unit checks, golden output checks, and architectural tests
that protect layering and long-lived invariants.

## Status

Phase 0 is complete. Prevox is now in phase 0.5: the IR playground and
deterministic middle-end. The immutable domain model, canonical manual trace,
golden fixture, and first
temporal Motif transformations are implemented. Music IR is versioned, and
transform preflight checks can report structured diagnostics. Read-only
analyses measure density, motif reuse, first-pass Dorian tonal cohesion, and
genre-neutral melody hook features without judging or mutating the music. Pitch
transformations await an explicit interval and tuning model.
The first MIDI export spike can write the manual trace to
`artifacts/midi/manual_trace.mid` for DAW preview, and a renderer-local MIDI
profile can export logical voices as separate preview tracks in
`artifacts/midi/multi_voice.mid`. A temporary backend-local General MIDI drum
preview can export `artifacts/midi/drum_preview.mid` without making drums part
of Music IR yet. A theory-cohesion example can analyze and export lead, bass,
and drums to `artifacts/midi/theory_cohesion.mid`. MIDI import, Logic
integration, a GUI, plugin hosting, AI integration, and Strudel integration
remain deferred.
