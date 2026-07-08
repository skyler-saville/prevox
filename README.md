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
- [REFERENCES.md](REFERENCES.md) is the project's annotated research notebook.
- [docs/adr/](docs/adr/) records accepted architectural decisions and their
  consequences.

## Run the architecture trace

Prevox currently implements immutable core types and one completely manual
eight-bar D Dorian trace. The first deterministic middle-end transformations
support reversing, repeating, augmenting, and diminishing Motifs. It
deliberately contains no Composer, randomness, MIDI, or rendering yet.

```bash
poetry install
poetry run python -m unittest discover -s tests -v
poetry run python examples/manual_trace.py
```

## Status

Prevox is in phase 0.5: the IR playground and deterministic middle-end. The
immutable domain model, canonical manual trace, golden fixture, and first
temporal Motif transformations are implemented. Music IR is versioned, and
transform preflight checks can report structured diagnostics. Pitch
transformations await an explicit interval and tuning model. MIDI follows only
after the Music IR survives these pressure tests. Logic integration, a GUI,
plugin hosting, AI integration, and Strudel integration remain deferred.
