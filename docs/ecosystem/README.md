# Audio Software Ecosystem

This directory is a capability-oriented map of external audio and music software
that may be useful to Prevox, adjacent Frayed Banner projects, or the wider
production workflow.

It is intentionally **not** a dependency list and **not** a roadmap. A project can
be worth documenting without being something Prevox should adopt.

For accepted Prevox capabilities, see [../capabilities.md](../capabilities.md).
For research questions that influence architecture, see
[../../REFERENCES.md](../../REFERENCES.md). When a technology choice becomes an
architectural commitment, record it in [../adr/](../adr/).

## Ownership labels

Use an ownership label so internal projects and external tools can coexist in
the same catalog without implying the same relationship:

- **Frayed Banner project**
- **External open source**
- **External commercial / freeware**
- **Standard / specification**
- **Research / paper**

## Relationship labels

Use one or more of these labels for every project:

- **Dependency** — currently required by Prevox.
- **Candidate integration** — plausible implementation behind a Prevox port or adapter.
- **Reference implementation** — useful source/design to study.
- **Adjacent project** — solves a neighboring problem or overlaps with Prevox.
- **Production workflow tool** — useful to musicians even if Prevox never embeds it.
- **Research only** — worth understanding, but no integration intent.
- **Watchlist** — promising or fast-moving; re-evaluate later.

## Capability map

| Area | Page | Examples |
| --- | --- | --- |
| Audio analysis and MIR | [audio-analysis.md](audio-analysis.md) | librosa, Essentia, aubio, Vamp |
| Audio transcription and separation | [audio-transcription.md](audio-transcription.md) | Basic Pitch, NeuralNote, Demucs, Spleeter |
| Audio processing and infrastructure | [audio-processing.md](audio-processing.md) | FFmpeg, Pedalboard, Rubber Band, libsndfile |
| MIDI and symbolic music | [midi-symbolic-music.md](midi-symbolic-music.md) | Mido, pretty_midi, music21, FluidSynth |

## Internal project map

Internal projects get dedicated positioning pages so their boundaries can be
compared against external systems using the same research method.

| Project | Definition | Comparison page |
| --- | --- | --- |
| Prevox | Procedural composition engine separating musical intent from realized symbolic music | [projects/prevox.md](projects/prevox.md) |
| Audo_EQ | Programmable, reference-driven mastering engine with explicit analysis, decisioning, DSP, and diagnostics | [projects/audo-eq.md](projects/audo-eq.md) |

See [comparison-framework.md](comparison-framework.md) for the standard questions
used when comparing internal and external projects.

This `docs/ecosystem/` tree is a temporary home. Its structure is deliberately
portable so it can move into a dedicated Frayed Banner music-technology
knowledge repository later without changing the project boundaries it documents.

## Cross-cutting terms

These terms deliberately link multiple capability areas:

- **MIR (music information retrieval)** — extracting musical information from
  audio. See [audio analysis](audio-analysis.md#music-information-retrieval-mir)
  and [transcription](audio-transcription.md#automatic-music-transcription-amt).
- **AMT (automatic music transcription)** — converting performed audio into
  symbolic notes/events. See [audio transcription](audio-transcription.md#automatic-music-transcription-amt)
  and [symbolic music](midi-symbolic-music.md#symbolic-representation).
- **Stem separation** — estimating source-isolated audio before analysis,
  transcription, replacement, or repair. See
  [audio transcription](audio-transcription.md#source-separation).
- **DSP (digital signal processing)** — transforms or measures the waveform
  itself. See [audio processing](audio-processing.md#digital-signal-processing-dsp)
  and [audio analysis](audio-analysis.md).
- **Plugin hosting** — executing AU/VST3/LV2/etc. outside a traditional DAW.
  See [Pedalboard](audio-processing.md#pedalboard) and
  [Carla](audio-processing.md#carla).
- **Rendering** — turning symbolic instructions into audible output. See
  [FluidSynth](midi-symbolic-music.md#fluidsynth), plugin hosting, and Prevox's
  own backend/rendering boundary in [../../ARCHITECTURE.md](../../ARCHITECTURE.md).

## Evaluation checklist

Before promoting a project from research into a Prevox experiment, record:

1. **Capability** — what problem does it solve?
2. **Interface** — CLI, Python API, C/C++, plugin, service, or application?
3. **Input/output contract** — audio, MIDI, MusicXML, arrays, model tensors, etc.
4. **License** — especially important for GPL/AGPL or model-specific licenses.
5. **Maintenance** — active, mature/stable, experimental, or abandoned?
6. **Platform fit** — macOS and Apple Silicon status where relevant.
7. **Determinism** — can outputs be reproduced and tested?
8. **Isolation** — can it sit behind a port/adapter rather than leak into the domain?
9. **Failure modes** — what material does it handle poorly?
10. **Project relationship** — dependency, candidate integration, reference, or no adoption.
11. **Closest comparisons** — which existing projects solve the nearest problem?
12. **Boundary difference** — where does this project deliberately stop?
13. **Best-fit workflow** — when is this project the stronger choice?
14. **Architectural consequence** — does the comparison change a port, ADR,
    roadmap item, or domain boundary?

## Architectural rule

External software belongs behind replaceable infrastructure boundaries. Prevox
domain types should not depend directly on a particular transcription model,
separation model, plugin SDK, DAW, or file-format library.

A useful shape is:

```text
Domain capability
      |
      v
     Port
      |
  +---+------------------+
  |                      |
Adapter A             Adapter B
Basic Pitch           future AMT
Demucs                future separator
FFmpeg                alternative backend
```

That keeps this catalog useful even when individual projects become obsolete.
