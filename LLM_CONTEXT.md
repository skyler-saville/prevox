# LLM Context

> Last updated: 2026-07-11
>
> Project phase: 0 complete; 0.5 — IR playground active
>
> Implementation status: core types, canonical trace, temporal transforms,
> diagnostics, analyses, architecture guardrails, and minimal MIDI export are
> executable

## Purpose

This is the living handoff document for Prevox. It helps a new LLM session
quickly understand:

- what the project is and is not;
- what has been decided;
- what remains a proposal;
- what is implemented today;
- which mistakes must not be reintroduced;
- what should happen next.

This file is an index and status snapshot, not a replacement for the canonical
design documents. Update it after substantive decisions, implementation
milestones, bugs, or changes in direction.

## Source-of-truth order

When sources disagree, use this order and call out the conflict:

1. executable tests and current code for implemented behavior;
2. accepted Architecture Decision Records, once they exist;
3. [PHILOSOPHY.md](PHILOSOPHY.md) for enduring decision principles;
4. [ARCHITECTURE.md](ARCHITECTURE.md) and
   [MUSICAL_GRAMMAR.md](MUSICAL_GRAMMAR.md) for current semantics;
5. [VISION.md](VISION.md) for product direction and non-goals;
6. [ROADMAP.md](ROADMAP.md) for intended sequencing;
7. this file for current status, history, and handoff notes;
8. [REFERENCES.md](REFERENCES.md) for research, not adopted design.

Do not infer that an item is implemented because it appears in architecture or
roadmap documentation.

## Project in one paragraph

Prevox is an open-source procedural composition engine for musicians. It treats
a composition as a reproducible program and helps musicians explore ideas while
retaining authorship. It is becoming a small music compiler rather than a MIDI
generator: high-level musical intent is realized as backend-independent
symbolic music, evaluated through explicit proposals and critiques, then
rendered at the boundary. MIDI is the first target, not the domain model.

## North-star pipeline

The currently accepted conceptual pipeline is:

```text
Intent IR
    ↓
Composer + CompositionState
    ↓
Proposal
    ↓
Validators + Critics
    ↓
Arbiter
    ↓ accepted; state advances
Music IR
    ↓
Renderer + RenderingProfile
    ↓
performance projection
    ↓
MIDI
    ↓
Logic or another DAW
```

A future Intent DSL may compile to Intent IR. Python constructs the IR directly
until syntax is justified.

## Current repository state

As of 2026-07-08:

| Area | Status |
| --- | --- |
| Philosophy and vision | Documented |
| Architecture and grammar | Documented; initial boundaries exercised |
| Research notebook | Seeded and expected to grow |
| Capability matrix | Current frontend, middle-end, and backend support documented |
| Intent IR | Initial immutable `Intent` and targets implemented |
| Music IR | Initial immutable hierarchy, relative-time view, and schema version implemented |
| CompositionState | Immutable acceptance transition implemented |
| Proposal/Critique/AcceptanceDecision | Immutable records implemented |
| Composer/Critic/Arbiter behavior | Not implemented |
| Motif transformations | Reverse, repeat, scale, augment, diminish |
| Diagnostics | Immutable diagnostic values and transform preflight reports |
| Analyses | Density, motif-reuse, tonal-cohesion, and melody-hook reports over Music IR |
| Canonical inspection | Aggregate formatters and manual golden trace |
| Architectural tests | Import layering, immutability, and Music IR field guards |
| Contribution guide | Engineering guardrails documented |
| Rendering and MIDI | Minimal MIDI file export implemented; multi-voice preview profiles, GM drum preview, and theory-cohesion preview implemented; import deferred |
| Production Python code | Domain types, inspection, manual example, and MIDI export |
| Automated tests | Standard-library unit, golden, and architectural tests |
| Executable examples | Manual trace plus MIDI export preview; examples cookbook direction documented |
| Golden fixtures | Canonical manual trace |
| ADRs | Seven accepted records under `docs/adr/` |
| Git repository | Initialized with `origin` set to `skyler-saville/prevox` |

The Python project uses Poetry, targets Python 3.12 to 3.x before 4.0, and
uses `mido` for Standard MIDI File export. Tests use `unittest`. Run:

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

Generated `.mid` files are ignored by default. Manual preview output should go
under `artifacts/`, for example `artifacts/midi/manual_trace.mid` or
`artifacts/midi/multi_voice.mid`. Drum preview output goes to
`artifacts/midi/drum_preview.mid`. Theory-cohesion preview output goes to
`artifacts/midi/theory_cohesion.mid`. Do not commit binary MIDI files unless
they are intentionally placed under an allowed fixture or example path.

## Git workflow for future LLM sessions

The project owner wants frequent, atomic commits and pushes.

- Keep commits small and coherent: one architectural decision, one behavior
  slice, one doc update, or one guardrail at a time.
- Validate the relevant slice before committing; run the full suite before
  pushing a branch update.
- Push after each validated atomic commit or small batch of closely related
  commits.
- Do not leave completed work sitting unpushed unless the user explicitly asks
  to pause before publishing.
- Preserve unrelated user changes. If the working tree is mixed, stage only the
  files that belong to the current slice.
- Keep PR descriptions current when pushed commits materially change the scope.

## Accepted architectural decisions

These decisions are current unless an experiment and subsequent documentation
explicitly supersede them.

### Document first, then pressure-test

The project deliberately began with Markdown rather than implementation. That
phase has served its purpose. New abstractions now require evidence from small
examples or a vertical slice.

### Phase 0 is closed

Phase 0 ended on 2026-07-08. The project now has self-reinforcing architecture:
documents, ADRs, immutable values, deterministic transforms, diagnostics,
analyses, canonical formatting, golden tests, architectural tests, and LLM
handoff context are aligned. Future work should protect the middle-end rather
than restart the foundation.

### Think in compiler stages

Roadmap planning should use frontend, middle-end, and backend categories rather
than feature buckets. The current value is concentrated in the middle-end:
Intent IR, Music IR, analysis, transformations, diagnostics, validation,
critics, and future optimization.

### Two canonical semantic levels

- **Intent IR** describes purpose: rhetorical roles, target curves,
  relationships, constraints, and preservation.
- **Music IR** describes realized symbolic music: songs, sections, logical
  voices, phrases, motifs, pitches, durations, and placements.

Source syntax is not an IR. MIDI is not an IR. Intent may be absent for imported
or directly authored Music IR.

### Relative musical time

Music IR uses exact rational offsets relative to a containing phrase, voice, or
section. Absolute song positions are derived by composing placements. Wall-clock
time comes from the tempo map. MIDI ticks exist only in MIDI rendering.

Intent IR may retain unresolved relationships such as `before`, `after`,
`meets`, `overlaps`, and `during`. Arrangement or realization resolves them
before accepted Music IR reaches a renderer.

### Voice is not track or instrument

Music IR owns logical `Voice` identities and musical roles. It does not own
MIDI tracks, channels, patches, plugins, or instrument assignments. A
`RenderingProfile` maps voices to those destinations so the same composition
can be re-orchestrated without changing Music IR.

### CompositionState is immutable

Composers do not mutate shared state. They return proposals. After validation,
criticism, and arbitration, acceptance derives the next state. This enables
reproducibility, rollback, branching, and local regeneration.

State is a derived working snapshot, not a third canonical IR. It may expose
read-only queries over accepted Music IR when a decision requires realized
pitches or rhythms.

### Composers and Generators are different

- A **Composer** makes context-sensitive musical proposals.
- A **Generator** is a focused primitive such as a random walk, Euclidean
  rhythm, or Markov transition.

This prevents every small algorithm from becoming an agent-like object.

### Proposals explain their actual process

A Proposal includes its Music IR fragment, objectives, decision record,
provenance, predicted effects, confidence, and proposed state effects. Reasons
must describe the real derivation rather than a plausible story invented
afterward.

Composers do not grade their own work. Their predictions are evaluated
independently.

### Validators, Critics, and Arbiters are distinct

- **Validators** establish facts, invariants, and constraint results.
- **Critics** make contextual judgments and retain evidence, confidence, and
  reservations.
- An **Arbiter** compares eligible proposals under an explicit policy and
  records an `AcceptanceDecision`.

Broken IR cannot be voted into validity. Critic disagreement must remain
visible rather than being discarded after calculating one total score. Human
override remains possible and is recorded.

### Determinism is structural

Randomness is injected. Semantic child seeds are derived from stable identities
rather than call order. Regenerating one phrase must not unexpectedly change
unrelated material.

### Performance details stay below Music IR

Core `Note` currently means pitch, relative position, and duration. MIDI
velocity, CC, pitch bend, pedal data, timing offsets, and humanization do not
belong in Music IR.

Whether the performance projection should become a formal, reusable
non-canonical Performance IR remains open.

### MIDI export is a backend boundary

The first MIDI renderer writes Standard MIDI Files from `MusicIR.iter_notes()`.
It owns ticks-per-beat, preview velocity, channel, and a temporary 12-TET
pitch-to-MIDI-number mapping. That mapping is backend-local and must not be
treated as the core pitch or interval semantics.

### Music IR changes are stability-sensitive

Music IR is intended to be the project's most stable abstraction. During
`0.x`, changes require executable evidence, an ADR, and updated canonical
fixtures. This is a high bar, not a prohibition against correcting an early
mistake.

### Architecture is tested, not just documented

The test suite includes source-level guardrails for import layering, frozen
core domain values, and Music IR fields that must not become rendering or MIDI
concerns. These tests are intentionally conservative: if one fails, either the
change is architectural and needs a documented decision, or it is drift.

### Temporal transformations precede pitch transformations

Reverse, repeat, exact time scaling, augmentation, and diminution operate on
immutable Motifs and require explicit result identifiers. Transpose, invert,
and mirror remain absent until interval, tuning, and enharmonic-spelling
semantics are decided.

### Canonical inspection is observable behavior

Intent, Proposal, Critique, AcceptanceDecision, Motif, and Music IR aggregates
have deterministic human-readable formatting. The complete manual trace is a
golden test fixture. This format is not yet a persistence schema.

### Diagnostics are values

User-facing compiler workflows should report invalid input with structured
diagnostics instead of relying only on Python exception text. The first
diagnostic model includes severity, code, message, domain location, expected
values, notes, and immutable reports. Transform preflight helpers are the first
consumer. Low-level constructors may still raise exceptions for programmer
invariant violations.

### Analyses are pure measurements

Analysis passes read Music IR and return `AnalysisReport` values containing
named metrics plus optional diagnostics. They do not mutate Music IR and do not
judge whether the result satisfies an intent. Current analyses measure note
density, motif reuse, Dorian-oriented tonal cohesion, and genre-neutral melody
hook features; future Critics may consume these reports.

## Open decisions and active hypotheses

These are not settled. Do not present them as accepted architecture.

### MusicalContext versus CompositionState

Recent design feedback proposed a small read-only `MusicalContext` containing
only what a Composer or Critic needs: current key, tempo, section, relevant
motifs, previous cadence, target energy, target duration, and active voices.

Potential benefit: components do not inspect an entire song or depend on the
full state representation.

Open question: is this a distinct domain value, or simply a purpose-specific
projection of immutable `CompositionState`? Prefer the projection unless the IR
playground demonstrates different invariants or lifecycle.

### Formal Performance IR

The current architecture permits a renderer to derive a temporary performance
projection from Music IR. A recent proposal would formalize it as a typed,
non-canonical IR:

```text
Music IR
    ↓
Performer / performance lowering
    ↓
Performance IR
    ↓
MIDI or another backend
```

Candidate responsibilities include dynamics/velocity, articulation, swing,
pedal, microtiming, humanization, and backend-neutral expressive controls.

Adoption criterion: at least two performers or backends must need to share,
transform, inspect, or test these semantics. Until then, keep it a renderer
projection and avoid a third permanent model.

### Critic scoring and arbitration

The first Arbiter policy is intentionally unknown. Candidates include hard
requirements followed by weighted preferences, lexicographic priority, or
Pareto comparison. Do not normalize every Critic into one number prematurely.

### Musical generality

The architecture should not require staff notation, MIDI ticks, instruments, or
12-tone MIDI note numbers. The first implementation may nevertheless support
12-tone equal temperament and common meter. Claims about microtonality,
polymeter, non-Western systems, or unmetered music remain hypotheses until
examples demonstrate them.

### Serialization

No canonical project, Intent IR, Music IR, critique, or provenance file format
has been chosen. Human-readable inspection output is needed before persistence
design.

### Pitch transformations

Transpose, inversion, and pitch mirroring need a declared interval model,
tuning system, and spelling policy. Do not implement them by converting Pitch
to hidden MIDI numbers. Decide whether transformation semantics belong to a
12-TET-specific policy or a more general pitch-space abstraction only after
concrete musical examples are available.

## Historical corrections and regression guards

The following design mistakes or documentation regressions were found and
corrected:

| Earlier direction | Correction | Do not regress by |
| --- | --- | --- |
| Treat the project as a MIDI generator | Treat it as composition semantics with MIDI at the boundary | Adding MIDI fields to domain objects |
| Use one Music IR for both purpose and realization | Separate Intent IR from Music IR | Storing unresolved mood or goals as note properties |
| Put randomness on `Phrase.random()` | Coordinate generation through a Composer and application service | Giving IR entities hidden random behavior |
| Let a BassVoice update shared state | Return a Proposal; acceptance derives new immutable state | Mutating global or shared composition state |
| Use `Track` as the compositional container | Use logical `Voice`; tracks are export artifacts | Adding channel, patch, or instrument to Voice |
| Put velocity on core `Note` | Keep Note symbolic and lower expression later | Treating Music IR as MIDI with nicer names |
| Let temporal constraints reach rendering | Resolve them into relative placements first | Making a renderer solve arrangement |
| Let a Proposal report its own quality as fact | Separate predicted effects from Critic measurements | Treating rationale as independent evidence |

When a future implementation contradicts one of these guards, either fix the
implementation or record an explicit superseding decision.

## Resolved implementation issues

### 2026-07-06 — Manual example could not import Prevox

- Symptom: `poetry run python examples/manual_trace.py` raised
  `ModuleNotFoundError: No module named 'prevox'`.
- Root cause: Poetry had created a virtual environment but the local project
  had not been installed into it.
- Fix: run `poetry install`; document setup in README and this file.
- Regression coverage: the standard run instructions execute the installed
  package before the manual trace.
- Related decision: executable examples are project documentation and must run
  from a fresh clone.

### 2026-07-06 — Console hierarchy used incorrect tree connectors

- Symptom: repeated siblings were all printed with a final-child `└──`
  connector.
- Root cause: the first formatter emitted glyphs directly instead of rendering
  a tree structure.
- Fix: build inspection nodes first, then calculate sibling connectors during
  rendering.
- Regression coverage: `test_console_trace_exposes_the_complete_manual_pipeline`
  exercises the formatter; exact golden output remains deferred.

## Immediate next milestone

Milestones 1 and 2 are complete. The first middle-end slice is also complete:
temporal Motif transformations, canonical aggregate formatters, and one golden
trace are tested.

The next middle-end decision is the minimum pitch/interval model required for
transpose, inversion, and explicit repair. The first chromatic scale-membership
and vertical-interval analysis exists, but transformation semantics still need
to be tested against at least:

```text
D Dorian diatonic material
chromatic semitone transposition
enharmonic spelling
one non-12-TET counterexample or explicit limitation
```

Do not add a general tuning framework speculatively. If those cases cannot
justify clean semantics, continue strengthening traversal and validation and
leave pitch transformations deferred. The first `RandomWalkComposer` follows
the deterministic middle-end work and still excludes MIDI.

The implemented slices have established that:

- Intent IR makes musical sense without notes;
- Music IR makes musical sense without MIDI;
- every accepted event traces to intent and an actual decision;
- Critic measurement can disagree with Composer prediction;
- exact local placements produce a derived song timeline;
- Voice contains no instrument or MIDI assignment.
- transformations do not mutate source Motifs;
- reverse twice restores musical material;
- augment followed by diminish restores musical material.

## Examples that should try to break the model

Do not design all of these before the first slice. Add them incrementally as
executable documentation:

1. D Dorian monophonic riff;
2. “Twinkle, Twinkle, Little Star”;
3. repeating ostinato;
4. pedal-tone bass with evolving melody;
5. 12-bar blues;
6. simple canon;
7. Euclidean drums;
8. seeded random walk;
9. one real improvised guitar idea from the project owner.

Each mature example should eventually retain:

```text
Intent IR
Proposal log
Critic results
Arbiter decision
Music IR
Performance projection or Performance IR
MIDI
optional reference audio
```

Golden outputs should live under `tests/golden/` once serialization is stable.
Do not make binary MIDI bytes the only assertion; compare semantic IR and event
projections as well.

## Architecture Decision Records

Seven accepted ADRs now record the decisions exercised by code:

```text
docs/adr/
├── 0001-separate-intent-and-music-ir.md
├── 0002-relative-musical-time.md
├── 0003-voice-not-track.md
├── 0004-immutable-composition-state.md
├── 0005-temporal-motif-transformations.md
├── 0006-diagnostics-as-values.md
└── 0007-add-read-only-analysis-passes.md
```

Performance IR remains open and has no ADR. If one is created before supporting
evidence exists, it must be marked Proposed rather than Accepted.

## Known issues and risks

- Only manual and deterministic transformation slices exercise the
  architecture. No algorithm has yet tested the Composer boundary.
- Proposal currently carries a complete candidate Music IR. This is simple and
  correct for the first slice but may be too coarse for local regeneration.
- `CompositionState`, context projections, and provenance could duplicate the
  same information if boundaries are not enforced.
- Critics and arbitration could become an unnecessary agent framework. The
  first slice must remain one deterministic policy with very few evaluators.
- Intent dimensions such as energy, tension, and novelty lack agreed
  measurement semantics.
- Motif identity and preservation remain hypotheses.
- Transformation provenance is not yet retained beyond explicit derived
  identifiers.
- Music IR currently leans toward Western pitch and metrical concepts despite
  broader aspirations.
- MIDI import cannot recover authorial intent, motif identity, logical voices,
  or provenance reliably.
- Golden tests can become brittle if they assert incidental serialization
  rather than musical semantics.

## Explicitly deferred

Do not build these during the first vertical slice:

- Logic-specific integration beyond importing a normal MIDI file;
- GUI or graph editor;
- plugin hosting or third-party plugin API;
- AI composers, LLM Critics, or learned preference models;
- Strudel integration;
- real-time scheduling;
- audio synthesis, mixing, or mastering;
- MusicXML export;
- database or distributed execution;
- a general-purpose performance-style framework.

## Future prospects

If the first slices validate the model, plausible later directions include:

- multiple role-specific Composers proposing in parallel;
- focused Theory, Motif, Rhythm, Novelty, and preference Critics;
- human override histories that improve personal acceptance policies;
- interchangeable performance styles over one Music IR;
- orchestral, band, synth, ambient, and live renderings;
- microtonal, polymetric, unmetered, and culturally specific musical models;
- graph-based inspection and local regeneration;
- Logic template workflows;
- AI as one optional Composer or Critic rather than the system's brain.

These are prospects, not commitments.

## Update protocol

After substantive work:

1. update the date and phase at the top;
2. update the repository-state table with verified facts;
3. move decisions among proposed, accepted, rejected, or superseded;
4. record bugs with symptom, root cause, fix, and regression coverage;
5. add links to new ADRs and executable examples;
6. update the immediate next milestone;
7. preserve historical corrections instead of silently rewriting them;
8. keep this file concise enough to ingest in one pass.

For a bug, use:

```markdown
### YYYY-MM-DD — Short bug name

- Symptom:
- Root cause:
- Fix:
- Regression coverage:
- Related decision:
```

For a decision change, use:

```markdown
### YYYY-MM-DD — Decision title

- Previous status:
- New status:
- Evidence:
- Consequences:
- ADR:
```

## New-session checklist

A future LLM should:

1. read this file;
2. inspect the repository rather than trusting the status snapshot;
3. read the relevant canonical documents;
4. preserve the composition/performance and voice/instrument boundaries;
5. check whether the requested work changes an accepted decision;
6. avoid implementing deferred infrastructure;
7. update this file before ending substantive project work.
