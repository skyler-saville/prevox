# Architecture

## Architectural aim

Prevox separates musical meaning from algorithms, workflows, and file formats.
The domain must be usable without MIDI, a DAW, a database, a GUI, or a
particular generator.

Prevox has two canonical semantic levels:

```text
Python plan builder ─┐
future Intent DSL ───┼──→ Intent IR
                     │         ↓
                     │   composers + theory policies
                     │      Proposals
                     │         ↓
                     │   Critics + Arbiter
                     │         ↓ accepted
direct music builder ┼──→ Music IR + CompositionState
MIDI import ─────────┘              ↓
                           Renderer + RenderingProfile
                                    ├──→ MIDI
                                    ├──→ MusicXML
                                    └──→ live output
```

**Intent IR** represents desired musical function and direction without
requiring realized notes. **Music IR** represents realized symbolic music
without adopting a backend encoding. Together they form the domain model rather
than mirroring a separate set of domain entities.

An intent plan is optional. Imported or explicitly authored notes can enter
Music IR directly with unknown intent. Lowering is intentionally one-way:
analysis may infer candidate intent from music, but inference must never be
presented as recovered authorial intent.

## Why IRs rather than ASTs

An abstract syntax tree preserves the structure of one source language. Prevox
may eventually have several sources, and composers have no syntax at all. The
shared representations therefore preserve normalized musical meaning rather
than the spelling of an input program.

The convenient views may be hierarchical:

```text
Intent IR: CompositionPlan → SectionIntent → PhraseIntent
Music IR:  Song → Section → Voice/Phrase → Motif → Event
```

The actual model need not be a strict tree. Reused motifs, simultaneous
timelines, source relationships, and transformation provenance introduce
references that form a graph. Ownership remains hierarchical where that gives
clear lifecycle and invariants; identity and provenance use explicit
references.

Two levels are justified because unresolved purpose and realized musical events
have different invariants. Combining them would either force intent to pretend
to be notes or make backends reason about unresolved goals.

No third canonical Performance IR is planned initially. A renderer may derive a
temporary event schedule containing note-on, note-off, velocity, control, and
pitch-bend data. That projection should become a domain IR only if multiple
backends need to transform and preserve the same performance semantics.

## Time model

Music IR knows musical time, but only in composable local coordinates.

- Positions and durations are exact rational beat values.
- An event offset is relative to its containing phrase.
- A phrase placement is relative to its section or voice.
- A section placement is relative to its song.
- Absolute song positions are derived by composing those placements.
- Wall-clock time is derived from the tempo map.
- MIDI ticks are introduced only by a MIDI renderer.

This makes a motif or phrase reusable at any placement without rewriting its
events. A flattened absolute timeline is a derived view for analysis and
rendering, never the source of truth.

Intent IR may contain unresolved interval relationships such as `before`,
`after`, `meets`, `overlaps`, and `during`. Arrangement and realization resolve
those constraints into local Music IR placements. Contradictory or
under-specified relationships produce diagnostics; a renderer is not expected
to solve compositional constraints.

## IR requirements

Both IRs must be:

- independent of MIDI ticks, channels, files, and devices;
- deterministic and serializable without relying on object memory identity;
- able to express hierarchy, concurrency, reuse, and transformation lineage;
- explicit about required context and unresolved information;
- extensible without turning every node into an untyped property bag.

Intent IR must express roles, targets, curves, constraints, preservation, and
relationships without inventing a realization. Music IR must provide exact
musical time and be traversable by transformations, validators, and backends.
Both retain links across lowering so an event can be traced to the plan and
decision that produced it.

Neither IR initially promises to encode every musical tradition or every detail
of notation and performance. Unsupported assumptions must be visible rather
than presented as universal music theory.

## Semantic areas

The initial domain is divided by musical responsibility, not by anticipated
features.

| Context | Owns |
| --- | --- |
| Intent IR | plan, rhetorical role, target curves, preservation, relationships |
| Music IR | `Song`, `Section`, `Voice`, `Phrase`, placement, identity |
| Melody | `Note`, melodic contour, `Motif`, interval relationships |
| Harmony | `Pitch`, `Chord`, `Scale`, key and harmonic relationships |
| Rhythm | beat positions, durations, meter, rhythmic patterns |
| Arrangement | section order, repetition, variation, voice roles |
| Constraints | hard requirements, weighted preferences, evaluation results |
| Provenance | source identity, seeds, transformations, and derivation |
| Composition state | immutable context used during progressive realization |
| Criticism | independent evaluations and evidence |
| Rendering | voice assignment and external encoding |

These are conceptual boundaries. They may begin as a few modules and split into
packages only when their implementations earn that complexity.

## Layers and responsibilities

### Intent IR

Intent IR is a normalized composition plan, not a collection of mood strings.
Its first concepts include:

```text
CompositionPlan, SectionIntent, PhraseIntent, MusicalRole,
RhetoricalRole, IntentCurve, Constraint, PreservationRule
```

Examples of rhetorical roles include question, answer, escalation, transition,
and resolution. These are declared semantics whose realization depends on
context; they do not map to hard-coded note sequences.

### Music IR

Music IR contains immutable or carefully controlled musical values and
entities. It owns invariants such as positive duration, valid tempo, ordered
placement, and motif identity. It contains no file I/O and no MIDI terminology.

Its first vocabulary is:

```text
Song, Section, Voice, Phrase, Motif, Note, Chord, Scale, Placement
```

A `Voice` is a logical musical identity with a role such as melody, bass,
harmony, pulse, or texture. It is not a MIDI track, channel, instrument, or
plugin. The first model should make its monophonic or polyphonic capability
explicit rather than relying on the word “voice” alone.

Music IR contains no piano, guitar, synthesizer, patch, or plugin assignment.
Those belong to a `RenderingProfile`. This deliberate separation allows the
same Music IR to be rendered as an orchestra, guitar band, synth arrangement,
or abstract event listing.

### Composition state

`CompositionState` is an immutable snapshot of the musical world at one
realization step. It may include:

```text
position and section
key, scale, meter, and harmonic context
current intent and target curves
previously accepted phrase references
motif registry and active musical roles
energy, density, tension, and other measured context
decision history and provenance
```

State does not contain MIDI or mutable backend state. It should not duplicate
the entire Music IR, but may reference accepted material and expose deliberate
queries when a composer needs realized pitches or rhythms. A bass composer
cannot meaningfully follow a melody if note data is forbidden from its context.
Composition state is a derived working snapshot, not a third canonical IR.

The transition is explicit:

```text
(state, accepted proposal) → next state
```

This makes rollback, branching, local regeneration, and comparison ordinary
operations.

### Application

The application layer coordinates use cases:

- generate a phrase from context, intent, constraints, and a seed;
- accept or reject a compositional proposal and advance state;
- collect critiques and apply an explicit arbitration policy;
- transform selected material;
- validate a composition;
- arrange phrases into sections;
- import or export through a port.

It owns orchestration and transaction boundaries, not musical rules.

### Composers, generators, and passes

A **Composer** makes context-sensitive musical decisions. A **Generator** is a
smaller algorithmic primitive a composer may use, such as a random walk,
Euclidean rhythm, or Markov transition. This preserves a useful term without
asking every algorithm to behave like an autonomous musical agent.

```text
Composer:
  (Intent IR fragment, CompositionState, RandomSource) → Proposal

Proposal:
  Music IR fragment
  objectives addressed
  decision record and provenance
  predicted effects with confidence
  proposed state effects

Generator:
  algorithm-specific input + RandomSource → candidate material

Transformer:
  (Intent IR or Music IR, TransformContext) → same-level IR

Validator:
  Intent IR → PlanValidationReport
  Music IR  → MusicValidationReport

Critic:
  (Intent IR fragment, CompositionState, Proposal) → Critique

Arbiter:
  (Proposals, Critiques, AcceptancePolicy) → AcceptanceDecision
```

A composer proposes; it never mutates shared state. The application validates
and accepts a proposal before deriving the next state. Every stochastic
component receives randomness explicitly and must not read global random state.
Transformers declare which IR level they operate on and retain provenance.
Validators report; application policy decides whether to reject, repair, or
accept.

Theory is a set of policies, measurements, and validators used during
realization—not a single oracle between the two IRs. Different composers may
realize the same intent under different theoretical systems.

Validators and Critics are related but not interchangeable. Validators establish
facts, structural invariants, and constraint results. Critics interpret those
facts in the context of an intent and proposal. Failed IR invariants make a
proposal ineligible; they cannot be outweighed by favorable critic scores.

### Critics and arbitration

A Critic is a pure evaluator, not a repair pass. Initial critique dimensions may
include constraint satisfaction, intent fit, motif preservation, rhythmic
coherence, and novelty. A critique records:

```text
critic identity and version
measurements and named scores
confidence and evidence
violations or reservations
suggested follow-up
```

The proposal's stated reason is evidence about the Composer's process, not proof
that its goal was achieved. Critics measure the realized fragment
independently.

An Arbiter compares proposals and applies an explicit policy. It returns an
`AcceptanceDecision` containing the selected proposal, all critiques, policy
version, decision reasons, and any human override. Scores are not assumed to be
commensurable: an Arbiter may use hard requirements, weighted preferences,
lexicographic priorities, or Pareto comparison. Disagreement remains visible.

The first slice needs only one or two Critics and one deterministic policy.
There is no initial agent framework, voting network, or AI dependency.

### Canonical inspection

Core aggregate values have deterministic human-readable formatters independent
of `repr()`. The manual pipeline trace is a version-controlled golden fixture.
Formatting changes are reviewed like other observable behavior, while the
format remains distinct from a future persistence or interchange schema.

### Diagnostics

Compiler-like workflows report user-facing problems with immutable diagnostics:

```text
severity
code
message
domain location
expected values
notes
```

Domain locations describe the musical object path that produced the issue, such
as `Song → Section → Motif`. Future DSL or project-file frontends may add source
spans, but source spans are not required for diagnostics to be useful.

Constructors may still raise exceptions for programmer-facing invariant
violations. Frontends, validators, transforms, passes, renderers, and command
line interfaces should prefer `DiagnosticReport` when reporting input or
pipeline problems to a musician.

### Initial transformations

The first middle-end passes operate on immutable Motifs and return new Motifs
with explicit derived identifiers:

```text
reverse
repeat
scale_time
augment
diminish
```

These transformations use exact rational time and never mutate their input.
Transpose, invert, and pitch mirroring are deferred until interval, tuning, and
enharmonic-spelling semantics are explicit. They must not be implemented as
hidden MIDI-number arithmetic.

Transform preflight checks may return diagnostics before an operation is
attempted. This is the first step toward pass-style behavior without introducing
a full pass manager prematurely.

### Infrastructure and interfaces

Infrastructure implements ports for MIDI, persistence, and eventually external
tools. Interfaces such as a CLI or GUI invoke application use cases. Neither
contains domain behavior.

### Producers, frontends, and backends

An IR producer creates or imports one of the IRs. Initial producers are Python
builders, composers, and MIDI import. A frontend translates another authored
representation; the Musical Intent DSL is a later frontend with its own parser
and source AST if it adopts textual syntax.

A Renderer combines Music IR with a `RenderingProfile` that maps logical voices
to performers, instruments, patches, channels, or destinations. It then lowers
the result into an external representation. MIDI is the first renderer output.
MusicXML, DAW templates, and live event streams remain future outputs.

## Composition pipeline

The pipeline is a set of composable stages rather than one mandatory monolith:

```text
source or Python builder
          ↓
      Intent IR ──→ plan validation / intent transformations
          ↓
composer + CompositionState + theory policies + seed
          ↓
       Proposals
           ↓
        Critics
           ↓
        Arbiter
           ↓ accepted + state advances
       Music IR ──→ musical transformations / analysis
          ↓
  Renderer + RenderingProfile
```

The Musical Intent DSL is not required for this pipeline: Python can construct
Intent IR directly. Directly authored or imported Music IR may bypass
realization. Unresolved intent is never silently treated as realized music.

## Determinism

Reproducibility is a cross-cutting invariant:

- the project has a root seed;
- each operation derives a stable child seed from semantic identity, not call
  order;
- random sources are injected;
- unordered collections never influence generated order;
- exported project data records engine and algorithm versions;
- deterministic tests compare domain events before comparing encoded files.

Semantic child seeds allow one section to regenerate without perturbing every
later section.

## MIDI boundary

MIDI has adapters in both directions:

```text
MIDI importer → Music IR voices/beats/pitches
Music IR + RenderingProfile → performance projection → MIDI
```

Export policy chooses resolution, event ordering, channel allocation, and
metadata encoding. Instrument, patch, and channel assignments come from the
RenderingProfile, not Music IR. Import is necessarily interpretive: MIDI can
recover events, tempo, meter, and track labels, but it cannot reliably
reconstruct voices, motifs, intent, constraints, or generation provenance.
Imported material is therefore a valid composition with inferred voice
grouping and unknown intent, not a restored Prevox program.

## Proposed package direction

Packages should be added incrementally toward this shape:

```text
src/prevox/
├── domain/
│   ├── intent/
│   ├── state/
│   ├── constraints/
│   └── music/
│       ├── composition/
│       ├── harmony/
│       ├── melody/
│       ├── rhythm/
│       └── arrangement/
├── application/
├── composers/
├── critics/
├── generators/
├── transforms/
├── validation/
├── rendering/
│   └── midi/
├── infrastructure/
├── cli/
└── __init__.py
```

`domain/intent/` is the normalized Intent IR, not the future DSL parser.
`domain/music/` is the realized Music IR. The exact subpackages should be
created only as the playground proves their boundaries.

Empty directories are not architecture, so this tree should grow with working
vertical slices rather than be created all at once.

## API direction

The first user story is:

```python
plan = CompositionPlan(key="D Dorian", bars=8)
plan.add(PhraseIntent(role="question"))
plan.add(PhraseIntent(role="answer"))

music = compose(plan, seed=48291)
MidiRenderer(profile="gm-preview").write(music, "test.mid")
```

This is an experience target rather than a frozen API. The convenience function
coordinates a composer, explicit state transitions, and seeded randomness; it
does not put generation behavior on an IR entity.

## Decisions deliberately deferred

- Logic, REAPER, Strudel, and plugin-host integration;
- GUI and graph editing;
- third-party plugin discovery and lifecycle;
- AI-assisted generation;
- AI-assisted criticism or arbitration;
- real-time scheduling and audio rendering;
- distributed execution or database persistence;
- a stable public plugin API.

The IR playground, first MIDI round trip, and several real algorithms should
expose the right abstractions before any of these are designed.
