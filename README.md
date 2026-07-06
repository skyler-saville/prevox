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

## Status

Prevox is in phase 0: the semantics and lowering boundary between Intent IR and
Music IR are being designed before implementation. The first coded phase will
be an inspectable IR playground; MIDI follows it. Logic integration, a GUI,
plugin hosting, AI integration, and Strudel integration are intentionally
deferred.
