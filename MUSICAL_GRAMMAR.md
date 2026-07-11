# Musical Grammar

## Purpose

This document defines the language shared by musicians, the domain model, and
generation algorithms. It begins narrow on purpose. Terms should enter the
model only when they support a concrete composition or validation use case.

This vocabulary defines two semantic levels. **Intent IR** describes what a
composition is trying to accomplish. **Music IR** describes its realized
symbolic music. Neither defines a textual DSL or parser.

## Intent IR

Intent IR can be inspected before any notes exist. Its first concepts are:

- A **composition plan** defines the desired form and global context.
- A **section intent** gives a span a function, direction, and relationship to
  other sections.
- A **phrase intent** requests one bounded musical action.
- A **musical role** identifies a part's responsibility, such as melody, bass,
  harmony, pulse, or texture.
- A **rhetorical role** describes what a span does in discourse, such as
  question, answer, escalation, transition, or resolution.
- An **intent curve** describes how a target such as energy, density, or tension
  changes over a span.
- A **preservation rule** identifies relationships that should survive
  realization or variation.
- A **temporal relation** constrains intervals with terms such as before, after,
  meets, overlaps, or during without assigning a global timestamp.

Intent roles are semantic requests, not universal definitions. A composer
declares how it interprets the roles it supports, and the resulting decision
record makes that interpretation inspectable.

## Music IR

Music IR combines:

- hierarchical ownership for songs, sections, voices, phrases, and events;
- exact timelines for placement and concurrency;
- stable references for reused motifs and derived material;
- provenance linking realized material to intent, seeds, and transformations;
- annotations whose schemas are explicit and versioned.

A tree is a useful way to inspect one composition, but it is not the only shape
of the data. A motif may be referenced from several phrases without being
duplicated, and derived phrases may retain links to their sources.

Music IR is closer to a score than a performance stream, but it is not a
notation model. Instruments, patches, note-on messages, CC events, pitch bends,
and pedals are rendering concerns unless later use cases justify shared
semantics.

## Foundation

### Time

Musical time is measured in beats, independent of MIDI resolution.

- A **position** is an exact rational offset from the start of its container.
- A **duration** is a positive rational number of beats.
- A **placement** locates a reusable value relative to a parent timeline.
- **Tempo** maps beats to elapsed time and is positive.
- **Meter** groups beats for notation and accent; it does not alter event
  positions.

Floating-point values should not be the source of truth for musical positions.
Tuplets and repeated transformations must remain exact.

Local offsets compose through placements:

```text
event offset in phrase
  + phrase placement in voice/section
  + section placement in song
  = derived song position
```

Intent IR may remain relational, but accepted Music IR is temporally resolved.
Renderers consume a derived flattened timeline; they do not decide whether one
phrase occurs before or overlaps another.

### Pitch and harmony

- A **pitch** combines pitch class and octave.
- A **pitch class** is enharmonically spellable; C-sharp and D-flat can sound
  alike without meaning the same thing.
- An **interval** is a relationship between pitches.
- A **scale** is an ordered pitch-class collection rooted on a tonic.
- A **key** adds tonal function and spelling context to a scale.
- A **chord** is a named or explicit collection of pitches or pitch classes at
  a musical position.

The first implementation may support twelve-tone equal temperament while the
domain avoids encoding MIDI note numbers as pitches.

### Events and containers

- A **note** initially contains pitch, relative position, and duration.
  Backend-independent expression may be added as a separate typed concept only
  after a composition use case proves it; MIDI velocity is introduced by a
  performance projection.
- A **motif** is a recognizable identity described by selected relationships
  among notes, such as intervals, rhythm, or contour. It is not merely a copied
  list of notes.
- A **phrase** is a bounded unit of musical material with local context.
- A **voice** is a logical timeline with a musical role. It has no instrument,
  patch, MIDI track, or channel assignment.
- A **section** is a formal span such as an intro, verse, or chorus and may
  place material on several voices.
- A **song** is the aggregate root for global context, form, voices, and
  reproducibility metadata.

Containment and placement are distinct. A phrase can be defined once and placed
more than once; a transformed placement can refer back to its source.

These definitions are hypotheses to test with real examples. They are not a
claim that this is the smallest vocabulary for all music.

## Operations

### Composer

A composer proposes realized material from intent and context:

```text
phrase intent + composition state + random source → proposal
```

The proposal contains a Music IR fragment and the actual decisions that produced
it. Its rationale names objectives and predicted effects; those predictions are
not independent evaluation. A composer does not export files or mutate shared
state.

### Generator

A generator is a focused algorithmic primitive used by a composer:

```text
Euclidean generator: pulses + steps + rotation → rhythm candidate
Random walk:         current value + bounds + random source → next value
```

This distinction keeps small functions small while reserving `Composer` for
context-sensitive musical decisions.

### Composition state

Composition state is an immutable snapshot containing current context, accepted
history, motif references, active roles, and target measurements. It contains no
MIDI. It may expose read-only queries over accepted Music IR when a decision
depends on actual pitches or rhythms.

### Critic

A Critic evaluates a proposal from one named perspective and produces an
immutable `Critique`. Theory, motif continuity, rhythm, novelty, and intent fit
can be separate Critics. Critiques include measurements, confidence, evidence,
and reservations rather than only a pass/fail result.

A Validator supplies facts and invariant checks that a Critic may use. An
invalid IR fragment is ineligible for acceptance; criticism cannot vote a
broken value into validity.

### Arbiter

An Arbiter applies an explicit acceptance policy to proposals and critiques. It
records an `AcceptanceDecision`; only acceptance advances composition state.
Critic disagreement and human overrides remain in provenance.

### Transformer

A transformer derives material from existing material. Initial candidates
include transpose, reverse, invert, repeat, quantize, and humanize. Each
operation declares which relationships it preserves.

### Constraint

Constraints express evaluation policy:

- a **requirement** is pass/fail, such as “all notes remain within this voice's
  declared range”;
- a **preference** is weighted, such as “favor stepwise motion”;
- a **target** has a desired value or range, such as density between 0.2 and
  0.35.

Constraints influence generation but remain independently evaluable.

### Validation

Validation produces facts and diagnostics, not silent mutation:

```text
ValidationReport
├── measurements
├── satisfied constraints
├── violations
└── suggested repairs
```

Repair is an explicit transformation selected by application policy or the
musician.

## Musical Intent DSL

### Role

The Intent DSL is a later authored frontend for Intent IR. The IR itself can be
constructed and tested through Python before a parser exists:

```text
musical intent
      ↓
source AST
      ↓
Intent IR
      ↓
composer + CompositionState
      ↓
Music IR
```

Intent is contextual. “Tense” may increase dissonance in a harmonic context,
syncopation in a rhythmic context, or registral instability in a melodic one.
It should not map to a single universal knob.

### Initial dimensions

The first vocabulary should use continuous dimensions with optional qualitative
aliases:

| Intent | Possible measurable effects |
| --- | --- |
| `density` | onsets or sounding events per beat |
| `energy` | density, register, dynamic, accent, rhythmic activity |
| `tension` | non-diatonic weight, dissonance, instability, delayed resolution |
| `surprise` | statistical rarity or distance from established material |
| `repetition` | recurrence of rhythmic, interval, or exact patterns |
| `motion` | amount and size of pitch movement |
| `stability` | chord-tone emphasis, metrical emphasis, tonal resolution |

Words such as `sparse`, `tense`, and `calm` are named profiles over these
dimensions. Their compiled form is inspectable and versioned.

### Direction over time

“Building” is not a fixed mood; it is a curve over a span:

```yaml
intent:
  over: 8 bars
  energy: {from: 0.25, to: 0.80, curve: ease_in}
  density: {from: sparse, to: medium}
```

The curve can be sampled by a phrase generator or distributed across sections
by the arranger.

### Preservation

Preservation tells a transformation which identity-bearing relationships may
not drift:

```yaml
preserve:
  motif: verse_hook
  aspects: [rhythm, contour]
  strength: 0.9
```

Preservation strength below `1.0` is a weighted preference. An absolute
requirement should be stated explicitly.

### Example

```yaml
phrase:
  length: 8 bars
  role: melody

intent:
  profile: tense
  density: sparse
  energy:
    from: 0.3
    to: 0.7
  surprise: low

preserve:
  motif: main_hook
  aspects: [rhythm]

constraints:
  require:
    - within_scale: D minor
    - max_interval: octave
  prefer:
    - rising_contour: 0.7
    - resolve_final_note: 0.9
```

A compiler resolves aliases and profiles into a normalized, inspectable intent
plan. Conflicts produce diagnostics—for example, `density: sparse` combined
with a minimum of eight onsets per beat—rather than being resolved invisibly.

## Open questions to answer through implementation

- Which motif features are stable enough to model as identity?
- Should harmony be represented primarily by symbols, pitch sets, or voiced
  events?
- How are tempo and meter changes placed inside a song?
- Which intent measurements generalize across melody, harmony, and rhythm?
- How much provenance is useful before it becomes burdensome?
- What minimum project serialization is needed to guarantee reproducibility?
