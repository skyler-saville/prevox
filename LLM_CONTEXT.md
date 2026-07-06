# LLM Context

> Last updated: 2026-07-06
>
> Project phase: 0 — language and boundaries
>
> Implementation status: no functional engine code exists

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

As of 2026-07-06:

| Area | Status |
| --- | --- |
| Philosophy and vision | Documented |
| Architecture and grammar | Coherent but provisional until exercised |
| Research notebook | Seeded and expected to grow |
| Intent IR | Designed only |
| Music IR | Designed only |
| CompositionState | Designed only |
| Composer/Proposal/Critic/Arbiter | Designed only |
| Rendering and MIDI | Designed only |
| Production Python code | None |
| Automated tests | None beyond an empty package |
| Executable examples | None |
| Golden fixtures | None |
| ADRs | None |
| Git repository | Initialized with `origin` set to `skyler-saville/prevox` |

The Python project uses Poetry, targets Python 3.12 or newer, and currently has
no dependencies. `src/prevox/__init__.py` and `tests/__init__.py` are empty.

## Accepted architectural decisions

These decisions are current unless an experiment and subsequent documentation
explicitly supersede them.

### Document first, then pressure-test

The project deliberately began with Markdown rather than implementation. That
phase has served its purpose. New abstractions now require evidence from small
examples or a vertical slice.

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

## Historical corrections and regression guards

There are no previous runtime bugs because no engine exists yet. The following
design mistakes or documentation regressions were found and corrected:

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

## Immediate next milestone

Stop expanding the architecture horizontally. Build Phase 0.5: the IR
playground.

The first experiment is eight bars of monophonic melody in D Dorian:

```text
Intent IR
    ↓
one Composer
    ↓
at least two Proposals
    ↓
one Validator and one Critic
    ↓
one deterministic Arbiter
    ↓
Music IR
    ↓
inspectable relative-time tree and decision log
```

MIDI is deliberately not required for Phase 0.5. The next vertical slice adds
performance lowering and MIDI output.

Phase 0.5 succeeds when:

- Intent IR makes musical sense without notes;
- Music IR makes musical sense without MIDI;
- every accepted event traces to intent and an actual decision;
- changing one phrase intent does not perturb unrelated phrases;
- Critic measurement can disagree with Composer prediction;
- voice assignment can change without changing Music IR;
- the implementation exposes awkward abstractions quickly and remains cheap to
  replace.

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

ADRs have been proposed but not created. Before or alongside Phase 0.5, record
only decisions whose alternatives and consequences are now understood. Initial
candidates are:

```text
docs/adr/
├── 0001-intent-ir-and-music-ir.md
├── 0002-immutable-composition-state.md
├── 0003-relative-musical-time.md
├── 0004-voice-not-track.md
└── 0005-performance-projection.md
```

If the Performance IR question remains open, its ADR must be marked proposed
rather than accepted.

## Known issues and risks

- The architecture has not been exercised by code. Elegance on paper is not
  evidence of usability.
- The vocabulary is growing faster than executable examples.
- `CompositionState`, context projections, and provenance could duplicate the
  same information if boundaries are not enforced.
- Critics and arbitration could become an unnecessary agent framework. The
  first slice must remain one deterministic policy with very few evaluators.
- Intent dimensions such as energy, tension, and novelty lack agreed
  measurement semantics.
- Motif identity and preservation remain hypotheses.
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
