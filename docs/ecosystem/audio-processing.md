# Audio Processing and Infrastructure

[← Ecosystem index](README.md) · Related:
[audio analysis](audio-analysis.md) ·
[audio transcription](audio-transcription.md) ·
[MIDI and symbolic music](midi-symbolic-music.md)

## Digital signal processing (DSP)

DSP operates directly on sampled audio or on signals in realtime. Typical tasks
include resampling, filtering, equalization, compression, convolution, time
stretching, pitch shifting, denoising, format conversion, and plugin execution.

This layer should remain distinct from Prevox's musical domain model.

## FFmpeg

**Relationship:** Candidate dependency / production workflow tool  
**Interface:** CLI + C libraries  
**Typical data:** media files/streams → decoded, transformed, inspected, encoded output

FFmpeg is the strongest general-purpose infrastructure candidate in this catalog.

Useful capabilities:

- decode/encode many audio formats;
- inspect streams and metadata;
- channel/sample-rate conversion;
- filtering and loudness workflows;
- deterministic command-line batch processing.

Potential Prevox use:

```text
AudioFileGateway
    |
FFmpegAdapter
```

FFmpeg should be considered infrastructure, not a musical abstraction.

Overlaps with [libsndfile/SoundFile](#libsndfile-and-soundfile), SoX, and some
[loudness/QC](audio-analysis.md#loudness-and-qc) tasks.

## libsndfile and SoundFile

**Relationship:** Candidate integration  
**Interface:** C library + Python wrapper  
**Typical data:** common PCM audio files ↔ arrays

This pair is useful when code needs direct sample access rather than invoking a
general media CLI.

A common Python boundary is:

```text
file
 ↓
SoundFile
 ↓
NumPy array
 ↓
analysis / DSP / ML
 ↓
SoundFile
 ↓
file
```

Choose this over FFmpeg when straightforward sampled-audio I/O is enough.

## Pedalboard

**Relationship:** Candidate integration / reference implementation  
**Interface:** Python/C++  
**Typical data:** audio arrays/files + plugin chains → processed audio

Spotify Pedalboard is especially relevant because it can combine built-in DSP
with programmatic plugin hosting.

Potential uses:

- EQ/compression/reverb chains;
- offline rendering;
- automated AU/VST3 processing;
- testable production presets;
- rendering software instruments from MIDI.

See [plugin hosting](#plugin-hosting) and
[MIDI rendering](midi-symbolic-music.md#rendering-symbolic-music).

A possible future boundary:

```text
AudioProcessingPort
      |
PedalboardAdapter
```

Do not expose plugin instances inside Music IR.

## Rubber Band

**Relationship:** Candidate integration / production workflow tool  
**Interface:** CLI / C++ library  
**Typical data:** audio → time-stretched and/or pitch-shifted audio

Rubber Band is useful for tempo conformance and pitch transformation while
attempting to preserve other signal characteristics.

Example:

```text
generated stem
   ↓
tempo/key analysis
   ↓
Rubber Band
   ↓
session-conformed stem
```

This is audio transformation, distinct from symbolic transposition in
[MIDI/symbolic music](midi-symbolic-music.md).

## SoX

**Relationship:** Production workflow tool / reference implementation  
**Interface:** CLI

SoX is a compact scripting-oriented audio utility. It overlaps with FFmpeg but
can be easier for straightforward audio-only transformations.

## Plugin hosting

Plugin hosting means loading and executing effect or instrument plugins under
program control rather than relying on a DAW session.

Relevant standards/projects include:

- **AU** — Apple's Audio Unit format;
- **VST3** — Steinberg plugin standard;
- **LV2** — open plugin standard;
- **CLAP** — open plugin API;
- **Vamp** — analysis plugins; see
  [audio analysis](audio-analysis.md#vamp-and-sonic-visualiser).

### Carla

**Relationship:** Reference implementation / production workflow tool

Carla is a broad plugin host and patchbay useful for studying plugin discovery,
routing, automation, and multi-format hosting.

### Pedalboard

For Python-controlled AU/VST3 rendering, see [Pedalboard](#pedalboard).

## Restoration and denoising

Projects worth tracking:

- **RNNoise** — neural noise suppression;
- **DeepFilterNet** — speech-oriented deep filtering;
- **SpeexDSP** — preprocessing, echo cancellation, resampling;
- **zita-convolver** — convolution engine.

These are useful for cleanup but should be evaluated against music-specific
failure modes. A speech denoiser can damage sustained tones, ambience, cymbals,
or distorted textures.

## Automation opportunity

Because these tools expose CLIs/APIs, repetitive workflows can be scripted:

```text
discover input files
     ↓
probe with FFmpeg
     ↓
normalize format
     ↓
optional stem processing
     ↓
run analysis/QC
     ↓
write manifest + hashes + provenance
```

That is a better long-term direction than encoding a sequence of manual DAW
steps into project knowledge.
