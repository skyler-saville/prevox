# Prevox

[← Ecosystem index](../README.md) ·
[Comparison framework](../comparison-framework.md)

> **Prevox is an open-source procedural composition engine that represents
> musical intent separately from realized symbolic music.**

It treats a song as a reproducible program. Composers propose material, analyses
and Critics can evaluate it, transformations develop it, and Renderers carry the
accepted symbolic result into external workflows.

Prevox composes music rather than audio.

## Problem it solves

Many generative music systems collapse several concerns into one step:

~~~text
prompt / pattern / model
          ↓
       output
~~~

Prevox separates them:

~~~text
Intent IR
    ↓
Composer
    ↓
Proposal
    ↓
analysis / criticism / arbitration
    ↓
Music IR
    ↓
Renderer
~~~

The core distinction is between:

- **Intent IR** — what the composition is trying to do; and
- **Music IR** — the symbolic musical structure that realizes it.

That separation allows Prevox to preserve compositional purpose, structure,
provenance, deterministic transformations, and backend independence.

See [ARCHITECTURE.md](../../../ARCHITECTURE.md) for the canonical architecture.

## Core model

Prevox's important boundaries are:

~~~text
musical intention
      ↓
procedural realization
      ↓
symbolic composition
      ↓
rendering / export
~~~

Music IR intentionally does not own MIDI channels or ticks, instruments or
plugin instances, DAW tracks, waveform audio, mastering, or a particular
generation model.

Those belong to adapters, rendering profiles, or other bounded contexts.

## Best use cases

### Reproducible procedural composition

Generate the same musical result from the same plan, algorithms, and explicit
random seed.

### Controlled musical variation

Preserve some properties while changing others: motif identity, rhythmic
character, or contour may remain stable while register, ending, density, or
harmonic tension changes.

### Inspectable generative workflows

Retain why material exists, which transformation produced it, and which analysis
or decision accepted it.

### Symbolic composition for a DAW

Generate or transform musical structures, export a representation such as MIDI,
then use Logic or another DAW for sound design and production.

### Research into musical intent and criticism

Experiment with the distinction between objective analysis, hard validation,
subjective Criticism, and arbitration without making one model the authority on
"good music."

## Poor-fit use cases

Prevox should not become the primary solution for audio synthesis, mixing,
mastering, waveform restoration, source separation, audio-to-MIDI
transcription, DAW replacement, or opaque one-shot AI song generation.

Those may be upstream or downstream integrations, but they are not the
composition domain.

## Closest comparisons

No single current project has the same boundary as Prevox. The useful
comparisons come from several neighboring families.

### Strudel / TidalCycles

**Overlap**

- composition as code;
- deterministic transformations;
- exact/cyclic time models;
- reusable musical patterns;
- separation between musical control and sound generation.

**Difference**

Strudel and TidalCycles are strongly pattern- and live-coding-oriented.
Prevox is centered on finite, inspectable composition structure, explicit
intent, provenance, analysis, and eventual proposal/criticism workflows.

~~~text
Strudel / Tidal
pattern → event stream → sound/control

Prevox
intent → symbolic composition → renderer
~~~

**Better fit**

Use Strudel/Tidal when immediate pattern transformation, cyclic sequencing, or
live performance is the primary goal.

Use Prevox when the song itself should remain an explicit, inspectable,
reproducible artifact with compositional semantics.

Primary references:

- https://strudel.cc/
- https://tidalcycles.org/

### Sonic Pi

**Overlap**

- algorithmic music;
- deterministic/reproducible code;
- MIDI and external control possibilities;
- musician-oriented programming.

**Difference**

Sonic Pi optimizes for immediacy: write code and hear it. It combines sequencing,
synthesis, sampling, effects, and live performance in one environment.

Prevox deliberately keeps sound production outside the musical domain model.

**Better fit**

Use Sonic Pi for learning, improvisation, performance, or fast sonic
experimentation.

Use Prevox when the composition needs long-lived symbolic structure independent
of its eventual sound.

Primary reference: https://sonic-pi.net/

### Magenta-family generative systems

**Overlap**

- automatic music generation;
- symbolic musical data;
- computational composition research.

**Difference**

Magenta-style systems are typically organized around learned models and the
sequences those models generate.

Prevox is model-agnostic. A machine-learning model could become one Composer or
Generator behind a Prevox interface without defining the architecture itself.

**Better fit**

Use a model-focused system when experimenting with a particular learned
generation technique.

Use Prevox when multiple generators, deterministic algorithms, constraints,
analysis, provenance, and human-authored material should coexist behind a stable
composition model.

Primary reference: https://github.com/magenta/magenta

### music21

**Overlap**

- symbolic music;
- pitch, interval, scale, chord, and score concepts;
- analysis and transformation.

**Difference**

music21 is primarily a symbolic-music and computational-musicology toolkit.
Prevox is a composition engine organized around progressive realization from
intent into a backend-independent Music IR.

**Better fit**

Use music21 for rich symbolic analysis, theory, notation, and corpus work.

Use Prevox when the main problem is orchestrating a reproducible composition
process and preserving the decisions that produced the result.

Primary reference: https://www.music21.org/

### MusPy

**Overlap**

- symbolic representation;
- transformations and machine-learning-oriented music data;
- multiple representations of musical events.

**Difference**

MusPy is especially useful for symbolic-music datasets and representations.
Prevox defines its own domain semantics so that no interchange or ML
representation becomes canonical.

**Better fit**

Use MusPy for dataset-oriented symbolic music research.

Use Prevox when intent, composition state, provenance, and renderer independence
matter more than representation interoperability alone.

Primary reference: https://muspy.readthedocs.io/

## Relationship to Audo_EQ

Prevox and Audo_EQ belong at different ends of a production workflow:

~~~text
idea / intent
    ↓
 Prevox
    ↓
symbolic music
    ↓
DAW / synthesis / mixing
    ↓
 Audo_EQ
    ↓
mastered audio
~~~

Prevox owns **musical decisions**.

Audo_EQ owns **mastering decisions**.

Neither should absorb the other's domain.

See [audo-eq.md](audo-eq.md).

## Architecture implications

Comparisons with live-coding, ML-generation, and theory systems reinforce several
current architectural choices:

- keep Intent IR separate from Music IR;
- keep Music IR independent from MIDI and audio backends;
- treat pattern engines, ML models, and theory libraries as replaceable
  producers/adapters rather than canonical domain models;
- preserve explicit randomness and provenance;
- keep live coding as a possible frontend rather than redefining the core IR.

## Research status

**Ownership:** current Prevox repository  
**Relationship:** Internal project  
**Reviewed:** 2026-09-29

Revisit these comparisons as Prevox gains an actual Composer pipeline, MIDI
import, richer rendering, or a live/pattern-oriented frontend.
