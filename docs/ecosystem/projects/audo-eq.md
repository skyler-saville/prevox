# Audo_EQ

[← Ecosystem index](../README.md) ·
[Comparison framework](../comparison-framework.md) ·
[Repository](https://github.com/FrayedBanner/audo-eq)

> **Audo_EQ is a programmable, reference-driven mastering engine with explicit
> analysis, decisioning, DSP processing, and diagnostics.**

Its goal is not merely to apply a fixed effects chain. It analyzes target and
reference material, derives bounded processing decisions, applies mastering DSP,
then measures the result.

## Problem it solves

A fixed mastering preset assumes the same correction is appropriate for every
track.

Audo_EQ instead uses:

~~~text
target audio + reference audio
             ↓
          analysis
             ↓
          decision
             ↓
       DSP processing
             ↓
      measurement / QC
             ↓
        mastered audio
~~~

The reference influences tonal and loudness decisions without becoming part of
the output.

## Core model

The current pipeline separates several responsibilities.

**Analysis** measures loudness, spectral balance, spectral centroid and rolloff,
low/mid/high energy, crest factor, clipping/silence, sibilance proxies, and
reference-derived EQ deltas.

**Decisioning** maps measurements into bounded mastering parameters such as
gain, shelf EQ, compression, limiter behavior, de-essing, and loudness
correction.

**Processing** uses Spotify Pedalboard as the main DSP engine.

**Diagnostics** surface measurements and applied decisions rather than returning
only an opaque audio file.

The same mastering core is exposed through CLI and FastAPI workflows, including
batch operation and optional artifact persistence.

## Best use cases

### Repeatable reference-based mastering

Apply one consistent, inspectable mastering process to many tracks using a
trusted stylistic or project reference.

### Batch mastering

Process generated tracks, demos, alternate mixes, or catalogs without rebuilding
a DAW chain for each file.

### Mastering experiments with diagnostics

Compare target/reference/output behavior using measurable information such as
LUFS, true peak, crest factor, spectral balance, limiter settings, and applied
processing.

### API-based audio pipelines

Use mastering as a service behind another application or automated content
pipeline.

### Generated-music finishing

Provide a deterministic finishing stage for rendered or AI-generated material
before manual review or distribution.

## Poor-fit use cases

Audo_EQ should not become the primary solution for multitrack mixing, detailed
manual mastering with continuous engineer intervention, source separation,
restoration, composition or arrangement, symbolic music analysis, or DAW
replacement.

Those may connect to Audo_EQ but should remain separate capabilities.

## Closest comparisons

### Matchering

Matchering is the closest open-source conceptual comparison because it also uses
a target/reference mastering workflow.

**Overlap**

- target + reference;
- automated mastering;
- tonal/loudness matching;
- reproducible file-oriented processing.

**Difference**

Audo_EQ is developing an explicitly layered analysis → decision → processing →
diagnostics model and exposes the same mastering behavior through application
interfaces such as CLI and FastAPI.

The architectural value is that mastering decisions can remain inspectable
rather than being represented only by the resulting waveform.

**Better fit**

Use Matchering when its established reference-matching behavior directly fits
the desired workflow.

Use Audo_EQ when programmability, service integration, bounded decision logic,
batch orchestration, and inspectable diagnostics are central requirements.

Primary reference: https://github.com/sergree/matchering

### LANDR-style automated mastering services

**Overlap**

- reduce the effort needed to reach a usable master;
- automated tonal/dynamics/loudness decisions;
- musician-facing mastering automation.

**Difference**

Commercial automated-mastering services generally hide most implementation and
decision details behind a hosted product.

Audo_EQ's useful differentiator is not "AI mastering." Its stronger identity is
transparent, programmable mastering infrastructure.

**Better fit**

Use a commercial service when convenience and a finished hosted workflow matter
more than implementation transparency.

Use Audo_EQ when the mastering process itself needs to be scripted, tested,
inspected, or integrated into other software.

### iZotope Ozone-style mastering workflows

**Overlap**

- EQ;
- dynamics;
- limiting;
- loudness/peak concerns;
- reference-assisted mastering;
- automated assistance.

**Difference**

Ozone is an interactive mastering environment and plugin suite designed for
engineer control inside production workflows.

Audo_EQ is currently an automated engine/service rather than an interactive
mastering workstation.

**Better fit**

Use Ozone when a human mastering workflow needs deep realtime control and visual
feedback.

Use Audo_EQ when repeatable automation or API/batch execution is more important
than manual interaction.

Primary reference: https://www.izotope.com/en/products/ozone.html

### Pedalboard scripts

**Overlap**

Audo_EQ directly uses Spotify Pedalboard for DSP.

**Difference**

Pedalboard itself supplies audio effects, plugin hosting, and audio-processing
primitives. It does not define Audo_EQ's mastering decision model.

A simple script applies a known processing chain. Audo_EQ adds measurement,
comparison, bounded parameter selection, processing, and post-measurement.

**Better fit**

Use raw Pedalboard when the DSP chain is already known.

Use Audo_EQ when the application must derive, explain, and repeat mastering
decisions from source/reference measurements.

Primary reference: https://github.com/spotify/pedalboard

## Relationship to Prevox

Prevox and Audo_EQ are complementary bounded contexts:

~~~text
musical intent
     ↓
   Prevox
     ↓
symbolic composition
     ↓
render / DAW / mix
     ↓
  Audo_EQ
     ↓
mastered audio
~~~

Prevox owns **musical decisions**.

Audo_EQ owns **mastering decisions**.

Audo_EQ should not need to understand Intent IR, motifs, rhetorical roles, or
composition state. Prevox should not need to understand compressors, limiter
ceilings, or reference-match EQ.

See [prevox.md](prevox.md).

## Architecture implications

The current comparisons suggest several useful boundaries:

- keep analysis, decisioning, and DSP execution separately testable;
- treat Pedalboard as infrastructure rather than as the mastering domain;
- keep loudness/true-peak measurement explicit enough to swap implementations;
- resist expanding Audo_EQ into multitrack mixing;
- prefer stable application/domain contracts around volatile DSP libraries.

A future Frayed Banner-wide audio infrastructure package may become justified
if Prevox and Audo_EQ begin duplicating file ingest, loudness, provenance, or
rendering adapters. Document overlap first; extract shared code only after real
duplication appears.

## Research status

**Ownership:** Frayed Banner project  
**Relationship:** Internal project  
**Current dependency:** Spotify Pedalboard  
**Reviewed:** 2026-09-29

Revisit comparisons as the mastering engine gains more sophisticated analysis,
new DSP providers, interactive control, or production deployments.
