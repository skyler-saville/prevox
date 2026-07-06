# Vision

## Why Prevox exists

Prevox helps musicians discover ideas they would not have written alone without
taking authorship away from them.

Most music-generation systems ask for a description and return a finished
artifact. Prevox instead supports the ordinary compositional loop:

```text
generate → listen → keep → modify → continue
```

It exposes musical material as a program that can be inspected, regenerated,
constrained, and transformed. A rendered MIDI file is one result of that
program, not the source of truth.

## Product thesis

A composition has an identity beyond its exact notes. That identity may live in
a motif, contour, harmonic rhythm, density curve, section relationship, or set
of constraints. Prevox should let a musician preserve those qualities while
exploring variations.

The foundation is two backend-independent semantic representations:

```text
Intent IR → Composer → Proposal → Critics/Arbiter
                                      ↓ accepted
                         CompositionState + Music IR
                                      ↓
                                  Renderer
```

Intent IR describes rhetorical function, direction, relationships, and desired
change. Music IR describes realized structure, time, pitch, rhythm, and
provenance. This separation keeps MIDI at the edge without forcing abstract
intent into note-shaped containers.

Creation and evaluation are also separate. Composers explain what a proposal is
trying to accomplish; Critics measure it from independent perspectives; an
Arbiter records why a proposal was accepted or rejected. The musician remains
free to override that policy.

A later authored surface may be a **Musical Intent DSL**. A musician can express
direction such as:

- sparse and tense;
- gradually building;
- familiar rhythm with greater harmonic surprise;
- preserve this motif while changing its contour.

Prevox will parse those expressions into Intent IR. Context-sensitive composers
then realize the plan as Music IR. Intent guides the algorithms; it does not
hide them. Both IRs must be useful through direct Python construction before a
textual DSL exists.

The beliefs behind these choices—and the rules for resolving future
tradeoffs—live in [PHILOSOPHY.md](PHILOSOPHY.md).

## Principles

### Human authority

The engine proposes and explains. The musician selects, rejects, edits, and
decides when the work is finished. Regeneration should be local so a good bass
line does not disappear when a chorus melody changes.

### Composition before sound

The core represents notes, rhythm, harmony, form, and intent. It does not
synthesize audio. MIDI is the first interoperability format; DAWs and other
backends remain outside the domain.

### Reproducibility

A project records its inputs, algorithm versions, parameters, and random seed.
The same project under the same engine version must produce the same musical
events. A new seed creates a deliberate variation.

### Musical concepts, not transport concepts

Domain objects use beats, pitches, intervals, phrases, motifs, and chords.
MIDI ticks, channels, files, and device behavior belong at the boundary.

### Transparent behavior

Intent and constraints should compile into inspectable decisions. A musician
should be able to ask why a phrase became denser or why a candidate was
rejected.

### Small composable operations

Generators create candidates. Transformers derive material. Validators report
properties and violations. Arrangers place material in form. These roles should
remain separable and reusable.

## Intended users

Prevox is for musicians who want to:

- generate and develop riffs, melodies, bass lines, rhythms, and progressions;
- create structured variations without losing a musical identity;
- experiment with algorithmic and evolving composition;
- learn theory by inspecting decisions and validation results;
- move generated material into tools they already use.

Python is the first authoring surface, but the musical model should not depend
on Python syntax.

## Non-goals

Prevox is not:

- a DAW, audio editor, synthesizer, or mixing environment;
- a one-shot text-to-song service;
- a replacement for music theory or the musician's ear;
- coupled to Logic Pro, REAPER, Strudel, or a plugin host;
- initially a real-time performance system;
- initially a community plugin platform or AI integration layer.

Those integrations may become adapters later. They must not shape the core
model prematurely.

## What success looks like

The first success is humble: generate eight deterministic bars of monophonic
melody in D Dorian, export them as MIDI, and hear them in a DAW.

The deeper success is reached when a musician can retain what makes an idea
recognizable, ask Prevox to explore a meaningful direction, and choose a result
that still feels unmistakably theirs.
