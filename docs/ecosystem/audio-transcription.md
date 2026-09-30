# Audio Transcription and Source Separation

[← Ecosystem index](README.md) · Related:
[audio analysis](audio-analysis.md) ·
[audio processing](audio-processing.md) ·
[MIDI and symbolic music](midi-symbolic-music.md)

## Automatic music transcription (AMT)

AMT converts recorded performance into symbolic note/event information. Outputs
may include pitch, note onset/offset, velocity, pitch bend, instrument identity,
or confidence.

AMT is related to [MIR](audio-analysis.md#music-information-retrieval-mir), but
it has a stronger reconstruction goal: produce symbolic events usable by
[MIDI/symbolic tooling](midi-symbolic-music.md).

A key architectural warning for Prevox: transcription recovers an **estimate of
performed events**, not original compositional intent. Imported notes should not
be silently promoted to Intent IR.

## Basic Pitch

**Official:** [Basic Pitch](https://basicpitch.spotify.com/) · [GitHub](https://github.com/spotify/basic-pitch)  
**Relationship:** Candidate integration / reference implementation  
**Interface:** Python / CLI  
**Typical data:** audio → MIDI/note events

Spotify's Basic Pitch is a practical baseline for polyphonic AMT and supports
pitch-bend information.

Best use pattern:

```text
isolated or mostly-isolated instrument
        ↓
   Basic Pitch
        ↓
   note events / MIDI
        ↓
post-process with Mido / pretty_midi
```

See [Mido and pretty_midi](midi-symbolic-music.md#mido-and-pretty_midi).

Potential Prevox shape:

```text
AudioTranscriptionPort
        |
BasicPitchAdapter
```

The port should expose Prevox-owned DTOs rather than Basic Pitch model objects.

## NeuralNote

**Official:** [GitHub](https://github.com/DamRsn/NeuralNote)  
**Relationship:** Adjacent project / reference implementation / watchlist  
**Interface:** desktop/plugin-oriented workflow, project-dependent internals

NeuralNote is valuable because it explores audio-to-MIDI from a producer-facing
workflow rather than only as a Python research library.

Use it to study:

- interaction design for transcription;
- correction/editing workflows;
- model latency and UX expectations;
- plugin/DAW integration patterns.

Prevox should not assume that matching NeuralNote's feature set is the right
product boundary.

## Source separation

Source separation estimates component signals such as vocals, drums, bass, and
other accompaniment.

This often improves AMT because most transcription models perform better on a
single musical source than on a dense mix.

Canonical pipeline:

```text
mix
 ↓
separator
 ↓
stems
 ├─ drums
 ├─ bass
 ├─ vocals
 └─ other
      ↓
 cleanup / analysis
      ↓
 transcription
```

## Demucs

**Official:** [Maintainer fork](https://github.com/adefossez/demucs) · [Original Meta repository](https://github.com/facebookresearch/demucs)  
**Relationship:** Candidate integration / reference implementation  
**Interface:** Python / CLI  
**Typical data:** mixed audio → estimated stems

Demucs is one of the major open source music-separation model families. Because
the ecosystem has forks and changing maintenance status, integration should be
adapter-based and version-pinned.

Potential Prevox use: a `StemSeparationPort`, not a direct domain dependency.

## Spleeter

**Official:** [GitHub](https://github.com/deezer/spleeter)  
**Relationship:** Reference implementation / alternative candidate  
**Interface:** Python / CLI  
**Typical data:** mixed audio → 2/4/5-stem estimates

Spleeter remains useful as a baseline and for comparing separation quality,
runtime, model size, and packaging complexity against Demucs-family systems.

## Open-Unmix

**Official:** [GitHub](https://github.com/sigsep/open-unmix-pytorch)  
**Relationship:** Research/reference implementation  
**Interface:** Python / model tooling

Open-Unmix is particularly useful as a clean research reference for music source
separation and evaluation, even when another model wins production testing.

## Separation is not restoration

A separated stem can contain:

- bleed from other sources;
- phase artifacts;
- transient smearing;
- missing harmonics;
- model hallucinations.

Therefore:

```text
separation ≠ original multitrack recording
```

Any later [analysis](audio-analysis.md) or transcription step should preserve
provenance that the source was model-derived.

## Speech and vocal transcription

Vocal workflows can also use speech-oriented systems such as [Whisper](https://github.com/openai/whisper)
transcription for words/timestamps. That is a different task from musical AMT.

Potential chain:

```text
vocal stem
 ├─ speech/lyric transcription → words + timestamps
 └─ musical transcription      → notes + pitch contours
```

Combining the two could eventually support lyric alignment, but neither should
be treated as ground truth without confidence/provenance.
