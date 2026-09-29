# Audio Analysis and MIR

[← Ecosystem index](README.md) · Related:
[audio transcription](audio-transcription.md) ·
[audio processing](audio-processing.md) ·
[MIDI and symbolic music](midi-symbolic-music.md)

## Music information retrieval (MIR)

Music information retrieval is the broad field of extracting useful musical
information from recordings or symbolic music. Typical features include tempo,
beats, onsets, pitch, tuning, chroma, spectral descriptors, harmonic/percussive
content, loudness, structure, and similarity.

For note-event extraction specifically, see
[automatic music transcription (AMT)](audio-transcription.md#automatic-music-transcription-amt).

## librosa

**Relationship:** Candidate integration / reference implementation  
**Interface:** Python  
**Typical data:** audio files or NumPy arrays → features/annotations

Useful capabilities include:

- beat and tempo estimation;
- onset detection;
- chroma and pitch-class features;
- spectral transforms and descriptors;
- harmonic/percussive source separation (HPSS);
- recurrence and structural-analysis utilities.

Potential Prevox use: an `AudioAnalysisPort` implementation for ingest-time
measurements or diagnostics. It should remain infrastructure; Music IR should
not become coupled to librosa types.

Overlaps with: [Essentia](#essentia), [aubio](#aubio), and preprocessing in
[audio transcription](audio-transcription.md).

## Essentia

**Relationship:** Candidate integration / reference implementation  
**Interface:** C++ / Python  
**Typical data:** audio → low-, mid-, and higher-level descriptors

Essentia is a larger MIR/DSP toolkit than librosa and is useful when the task
moves from individual features toward a consistent extraction pipeline.

Potential Prevox use: deeper tonal, rhythmic, timbral, or classifier-oriented
analysis where a simple librosa pipeline becomes fragmented.

Engineering note: evaluate licensing and binary-distribution implications before
embedding it.

## aubio

**Relationship:** Candidate integration / reference implementation  
**Interface:** C / Python / CLI  
**Typical data:** audio → pitch, onset, beat, tempo estimates

aubio is comparatively small and focused. It is useful as a baseline for
realtime or low-overhead feature extraction.

Overlaps with:

- [Basic Pitch](audio-transcription.md#basic-pitch) for pitch/note extraction,
  though aubio is not equivalent to modern polyphonic AMT;
- librosa for onsets and tempo;
- realtime input pipelines in [audio processing](audio-processing.md).

## Vamp and Sonic Visualiser

**Relationship:** Reference implementation / production workflow tool  
**Interface:** analysis-plugin standard + desktop application

The Vamp ecosystem is important because it separates **analysis plugins** from
audio effects. Sonic Visualiser can inspect waveform/spectrogram data and display
analysis outputs from Vamp plugins.

Potential Prevox use is primarily validation and debugging: when an automated
analysis looks suspicious, a visual inspection tool is valuable for determining
whether the algorithm, assumptions, or source material are at fault.

Related term: [plugin hosting](audio-processing.md#plugin-hosting) is a different
problem. VST/AU/LV2 usually process or synthesize audio; Vamp plugins primarily
extract features.

## Loudness and QC

Several libraries sit between analysis and processing:

- **libebur128** — EBU R128 / ITU BS.1770 measurement primitives.
- **pyloudnorm** — Python loudness measurement and normalization workflows.
- **FFmpeg loudnorm** — command-line analysis and normalization.

See [FFmpeg](audio-processing.md#ffmpeg) for infrastructure context.

Potential workflow:

```text
rendered audio
    ↓
probe format / channels / sample rate
    ↓
measure LUFS / true peak
    ↓
emit diagnostics
    ↓
optionally normalize or reject export
```

This is a strong candidate for automated quality-control tooling because the
results are objective enough to test while remaining outside Prevox's musical
judgment layer.

## Structural and similarity analysis

Future areas worth tracking include:

- section boundary detection;
- repeated-pattern discovery;
- audio fingerprinting;
- embedding-based similarity;
- sample-library search;
- alignment between alternate renders.

These may eventually connect analysis of recordings back to
[symbolic structures](midi-symbolic-music.md#symbolic-representation), but the
mapping is probabilistic and should not be treated as recovered authorial intent.
