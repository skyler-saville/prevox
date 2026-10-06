# Creative Audio Transformation

[← Ecosystem index](README.md) · Related:
[audio processing](audio-processing.md) ·
[audio transcription](audio-transcription.md) ·
[MIDI and symbolic music](midi-symbolic-music.md)

Creative audio transformation treats rendered audio as raw material rather than a
finished artifact. The goal is not only to preserve quality or correct problems,
but to deliberately alter identity, timing, spectrum, texture, dynamics, or
structure in controllable ways.

This capability sits between infrastructure DSP and mastering:

~~~text
generated / recorded audio
        ↓
creative transformation
        ↓
resampling / recombination
        ↓
mix / production
        ↓
mastering
~~~

It should remain distinct from Audo_EQ's mastering domain and from Prevox's
symbolic composition domain.

## Why this category exists

Infrastructure DSP asks:

> How do we process audio reliably?

Creative transformation asks:

> How do we make the source become something else?

Typical techniques include:

- granular synthesis;
- spectral transformation;
- extreme time stretching;
- creative pitch/formant manipulation;
- nonlinear distortion and waveshaping;
- convolution with unconventional impulse responses;
- feedback and recursive processing;
- transient extraction/reconstruction;
- resampling;
- intentional bit-depth/sample-rate degradation;
- repeated generational processing.

This distinction is musically useful even when the same low-level libraries are
used underneath both workflows.

## Signalsmith Stretch

**Official:** [Signalsmith Stretch](https://signalsmith-audio.co.uk/code/stretch/) · [GitHub](https://github.com/Signalsmith-Audio/signalsmith-stretch)  
**Ownership:** External open source  
**Relationship:** Experiment / candidate integration  
**Maintenance:** Active  
**License:** MIT  
**Interface:** C++ library, with third-party bindings available  
**Typical data:** audio → pitch/time/formant-transformed audio

Signalsmith Stretch is a polyphonic pitch/time processing library with support
for pitch shifting, time stretching, formant manipulation, and custom frequency
maps.

Why it matters:

- permissive licensing;
- strong fit for programmatic offline processing;
- useful for both conventional and deliberately unnatural transformation;
- small enough to evaluate without committing to a plugin framework.

Potential Frayed Banner boundary:

~~~text
CreativeTimePitchPort
        |
SignalsmithStretchAdapter
~~~

The library should remain infrastructure. Presets, mutation strategies, and
artistic intent should be owned by higher-level Frayed Banner code.

### Best experiment

Take one stem and record a reproducible mutation recipe:

~~~text
input stem
   ↓
pitch -7 semitones
formant +15%
time ×1.35
   ↓
output stem
   ↓
source hash + parameters + tool version
~~~

If this kind of repeatable destructive processing actually becomes part of the
music workflow, promote the capability from experiment to candidate integration.

## PaulXStretch

**Official:** [GitHub](https://github.com/essej/paulxstretch)  
**Ownership:** External open source  
**Relationship:** Experiment / production workflow tool  
**Maintenance:** Maintained  
**License:** GPLv3 with App Store license exception  
**Interface:** application / plugin  
**Typical data:** audio → extreme spectral/time transformation

PaulXStretch is designed for extreme time stretching and spectral transformation,
not transparent tempo correction.

Its value is artistic rather than infrastructural:

~~~text
short chord
    ↓
extreme stretch
    ↓
long evolving texture
    ↓
distortion / convolution / resampling
    ↓
new source material
~~~

This is a strong example of finished audio becoming a new instrument or texture.

Because of its licensing and specialized workflow, treat it as an external tool
rather than a foundational library.

## Faust

**Official:** [faust.grame.fr](https://faust.grame.fr/) · [GitHub](https://github.com/grame-cncm/faust)  
**Ownership:** External open source  
**Relationship:** Candidate integration / strategic watchlist  
**Maintenance:** Very active  
**License:** GPL ecosystem; generated-code and target licensing must be reviewed per deployment  
**Interface:** DSP language/compiler  
**Typical data:** DSP source → generated implementations / plugins / applications

Faust is strategically different from a normal audio library. It provides a
language for defining DSP and compiling it into multiple execution targets.

Potential future use:

~~~text
Frayed Banner DSP idea
        ↓
      Faust
        ↓
generated DSP implementation
        ↓
standalone / plugin / embedded target
~~~

This is relevant if Frayed Banner eventually develops custom audio processors
rather than only orchestrating third-party plugins.

Do not put Faust on the immediate Prevox or Audo_EQ roadmap. Revisit after
creative-processing experiments prove that custom DSP is artistically useful.

## DPF

**Official:** [DPF documentation](https://distrho.github.io/DPF/) · [GitHub](https://github.com/DISTRHO/DPF)  
**Ownership:** External open source  
**Relationship:** Watchlist / reference implementation  
**Maintenance:** Active  
**License:** ISC; plugin-format-specific licensing still applies  
**Interface:** C++ plugin framework  
**Typical data:** plugin source → standalone / plugin binaries

DPF is relevant as a possible packaging layer for custom DSP. It supports
multiple plugin formats from one codebase and is especially interesting when
paired conceptually with Faust.

Possible future path:

~~~text
custom DSP
   ↓
 Faust
   ↓
generated implementation
   ↓
  DPF
   ↓
CLAP / VST3 / LV2 / standalone
~~~

This is architecture research, not an immediate integration target.

## SuperCollider

**Official:** [supercollider.github.io](https://supercollider.github.io/) · [GitHub](https://github.com/supercollider/supercollider)  
**Ownership:** External open source  
**Relationship:** Research only / experiment  
**Maintenance:** Active  
**License:** GPLv3  
**Interface:** language + audio server + IDE  
**Typical data:** code / buffers / live audio → synthesis and processing

SuperCollider is useful as a DSP sketchbook.

It can prototype combinations such as:

- granular buffers;
- feedback networks;
- spectral freezing;
- pitch-controlled distortion;
- recursive processing;
- algorithmic modulation.

If a prototype becomes musically important, then decide whether to reimplement
it in Faust, Pedalboard, a standalone processor, or leave it as a production
tool.

This keeps experimental sound design ahead of software architecture rather than
the reverse.

## Granade

**Official:** [GitHub](https://github.com/Audio-Builders-Foundry/granular_synth)  
**Ownership:** External open source  
**Relationship:** Watchlist / experiment  
**Maintenance:** Young / experimental  
**License:** MIT  
**Interface:** VST3 / standalone / WebAssembly  
**Typical data:** live or buffered audio → granular textures

Granade is an open-source realtime granular synthesizer. It breaks incoming audio
into overlapping grains and exposes controls such as density, spread, offset,
grain size, mix, pan, and windowing.

This is useful for turning recognizable source material into evolving textures
while preserving some sonic identity.

The project explicitly describes itself as early-stage and better suited to
creative exploration than critical production use, so it should remain on the
watchlist rather than becoming an architectural dependency.

## Cardinal and VCV Rack

### Cardinal

**Official:** [GitHub](https://github.com/DISTRHO/Cardinal)  
**Ownership:** External open source  
**Relationship:** Research only / production workflow tool  
**Maintenance:** Active  
**License:** GPLv3+ final binary, with module-level license complexity  
**Interface:** modular plugin / standalone environment

### VCV Rack

**Official:** [vcvrack.com](https://vcvrack.com/) · [GitHub](https://github.com/VCVRack/Rack)  
**Ownership:** External open source / commercial ecosystem  
**Relationship:** Research only / production workflow tool  
**Maintenance:** Active  
**License:** GPLv3 core plus separate distribution/plugin terms  
**Interface:** modular synthesis environment

These environments are useful as production laboratories rather than application
dependencies.

A good rule:

> Prototype the strange signal flow in a modular environment first. Write code
> only after the technique proves musically useful.

This reduces the risk of building infrastructure around an interesting
engineering idea that never becomes part of the actual artistic workflow.

## Relationship to Prevox

Prevox should not manipulate waveform audio directly.

The useful connection is conceptual: controlled destruction can happen at the
symbolic level before rendering.

~~~text
SYMBOLIC MUTATION              AUDIO MUTATION

Prevox                         creative DSP
  │                                │
notes                            samples
rhythm                           spectrum
harmony                          phase
structure                        timbre
motifs                           transients
  │                                │
  └─────────── render ─────────────┘
~~~

This reinforces the existing architecture:

- keep Music IR symbolic;
- make destructive symbolic transforms explicit and provenance-aware;
- place audio mutation after rendering or behind dedicated infrastructure ports.

## Relationship to Audo_EQ

Audo_EQ should remain conservative and bounded.

~~~text
creative transformation
        ↓
       mix
        ↓
-----------------------
MASTERING BOUNDARY
-----------------------
        ↓
     Audo_EQ
        ↓
release master
~~~

Do not fold experimental degradation, granular processing, extreme stretching,
or feedback networks into the mastering domain.

Audo_EQ should continue to own bounded mastering decisions and diagnostics, not
sound-design mutation.

## Architecture findings

This research produces several concrete conclusions:

1. Add **Creative Audio Transformation** as its own ecosystem capability.
2. Keep it separate from infrastructure DSP and mastering.
3. Prefer reproducible mutation recipes with source hashes, parameters, tool
   versions, and provenance.
4. Experiment with external tools before extracting shared libraries or creating
   a new Frayed Banner project.
5. Use Signalsmith Stretch as the first bounded programmatic experiment.
6. Keep Faust + DPF as a future route for custom DSP/plugin development if the
   artistic workflow proves the need.
7. Use SuperCollider/Cardinal/VCV Rack as laboratories, not dependencies.

## Research classification

| Project | Classification |
| --- | --- |
| Signalsmith Stretch | Experiment → candidate integration if proven useful |
| PaulXStretch | Experiment / production workflow tool |
| Faust | Candidate integration / strategic watchlist |
| DPF | Watchlist / reference implementation |
| SuperCollider | Research only / experiment |
| Granade | Watchlist / experiment |
| Cardinal | Research only / production workflow tool |
| VCV Rack | Research only / production workflow tool |

**Reviewed:** 2026-10-05

The next useful step is not a large integration. It is one reproducible
Signalsmith-based stem-mutation spike and one deliberately extreme PaulXStretch
comparison. The result should answer whether programmatic destructive processing
belongs in the regular Frayed Banner music workflow.
