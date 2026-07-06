# Philosophy

## Purpose

Architecture says where code belongs. Philosophy says which tradeoff to choose
when several designs are technically valid.

This document is the project's decision compass. It should change rarely and
only when experience disproves a belief. [VISION.md](VISION.md) describes the
destination; this document describes how Prevox intends to travel.

## The problem

Prevox is not trying to generate MIDI. MIDI export is a useful experiment and a
boundary adapter.

The problem is:

> Help musicians discover ideas they would not have written manually, while
> preserving their ability to understand, select, and shape the result.

The difficult work is therefore semantic. Prevox must describe musical
relationships, identity, change, and intent well enough that different
algorithms can collaborate without reducing composition to a bag of notes.

## Problems we are not solving

- We are not building a DAW.
- We are not building an AI songwriter.
- We are not replacing musicians.
- We are not optimizing for imitation of commercially successful songs.
- We are not creating another piano roll.
- We are not synthesizing, recording, mixing, or mastering audio.
- We are not claiming one representation captures every musical tradition.
- We are not making output formats the source of musical truth.

When a proposed feature pulls Prevox toward one of these problems, it belongs in
another tool or at an adapter boundary unless there is compelling evidence
otherwise.

## Core beliefs

### The user remains the composer

Prevox proposes; the musician decides. Local regeneration, comparison,
provenance, and reversible operations matter more than autonomous completion.
The system should preserve chosen material unless the musician explicitly asks
it to change.

### Every generated event has a reason

A reason need not be a deterministic theory rule. It may be a seeded random
choice among candidates that satisfied a constraint. What matters is that the
event came from an inspectable process rather than an opaque accident.

Explanations must report actual provenance and measurements, not invent a
plausible story after generation.

Composers may state their objective and predicted effect, but independent
Critics evaluate the result. A component should not be the sole judge of its own
work.

### Randomness without relationships is noise

Randomness is valuable for exploration, but it operates inside musical context:
range, rhythm, contour, harmony, motif, form, or explicit user preference.
Seeds make chance repeatable; constraints make it purposeful.

### Music emerges from relationships

An isolated note carries little compositional meaning. Interval, timing,
repetition, contrast, expectation, orchestration, and formal placement create
identity. The model should privilege relationships without making elementary
events cumbersome.

### Identity and variation coexist

A useful system can answer both “what must remain recognizable?” and “what may
change?” Motif preservation, structural references, and transformation
provenance are foundational rather than decorative metadata.

### Theory is guidance, not law

Theory offers names, measurements, constraints, and useful defaults. It does not
decide whether music is valid. Rules may be requirements, weighted preferences,
or intentionally violated expectations. The musician's ear has final authority.

### Constraints should create possibility

Constraints are not merely rejection filters. They focus a search space,
articulate taste, and make controlled surprise possible. A good constraint helps
the musician explore; a bad one merely forbids.

### Meaning precedes encoding

Intent IR represents compositional purpose; Music IR represents realized
musical semantics. MIDI, MusicXML, notation, and live streams are lossy or
specialized projections. Backend limitations must be reported explicitly, not
leaked backward into either model.

Music IR is intended to be the project's most stable abstraction. Frontends,
Composers, Critics, transformations, and Renderers should evolve around it.
During `0.x`, stability means that an IR change requires executable evidence,
an ADR, and updated canonical examples—not that early mistakes are preserved
forever.

A useful boundary test is: “Would this concept still exist if MIDI had never
been invented?” If not, it almost certainly belongs in rendering. Passing that
test is necessary, not sufficient; a concept still needs a demonstrated use in
composition.

### Voices are musical; instruments are renderings

The composition owns logical voices and their roles. A rendering profile maps
those voices to instruments, patches, channels, plugins, or performers. The
same composition should survive radical re-orchestration without changing its
identity.

Instrument-specific composition may eventually be expressed as an explicit
intent or capability constraint. It should not enter through an accidental
`Track.instrument` field.

### Creation and criticism are different acts

Composers propose possibilities. Critics measure theory, intent fit, motif
continuity, rhythm, novelty, or other named concerns. An Arbiter applies an
explicit acceptance policy without erasing disagreement between Critics.

A single aggregate score is convenient but lossy. Prevox should retain the
underlying critiques and evidence so the musician can understand or override a
decision.

### Reproducibility enables trust

The same inputs, seed, and algorithm versions should produce the same musical
result. Reproducibility lets musicians keep what works, compare alternatives,
and understand the effect of one change.

### Simplicity is earned by semantics

A small public API is desirable, but not if it conceals ambiguous meaning.
Prevox should make common composition easy while keeping consequential decisions
inspectable. Convenience layers may be thin; the semantic core must be honest.

### Architecture must meet music early

An abstraction is provisional until a small musical example pressures it. The
project should alternate semantic design with inspectable and audible vertical
slices. A beautiful model that makes eight bars awkward is useful evidence, not
an architecture to defend.

### Observability is a product capability

Intent, proposals, critiques, acceptance, transformations, and Music IR should
have deterministic human-readable forms. These views support teaching, golden
tests, bug reports, and musical reasoning. They are public explanations, not
incidental object representations.

### The model is situated, not universal

Terms such as key, chord, scale, and bar reflect particular musical practices.
Prevox can begin there without calling them universal. Cultural and tuning
assumptions should be named, bounded, and replaceable where practical.

## Decision tests

When evaluating a design, ask:

1. Does this increase the musician's control or merely the system's autonomy?
2. Is this musical meaning, workflow policy, or backend encoding?
3. Can the result explain its real derivation?
4. Can one part regenerate without surprising changes elsewhere?
5. Does the design preserve relationships and identity?
6. Is a theory rule being mistaken for a universal law?
7. Are we adding a concept because music requires it or because a format does?
8. Can the idea be tested with a small audible example?

If the answers are unclear, the feature is not ready to become a core
abstraction.

## The standard of success

Prevox succeeds when it gives a musician a surprising idea, lets them understand
and reshape it, and then gets out of the way.
