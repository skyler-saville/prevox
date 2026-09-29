# MIDI and Symbolic Music

[← Ecosystem index](README.md) · Related:
[audio transcription](audio-transcription.md) ·
[audio analysis](audio-analysis.md) ·
[audio processing](audio-processing.md)

## Symbolic representation

Symbolic music represents musical events and relationships rather than sampled
waveforms. MIDI is one representation, but symbolic music also includes score
formats, theory objects, event graphs, notation, and higher-level structures.

Prevox's Music IR belongs to this broad family, but it should remain its own
domain model. External symbolic libraries are adapters, references, or import/export
tools rather than authorities over Prevox semantics.

See [MUSICAL_GRAMMAR.md](../../MUSICAL_GRAMMAR.md) and
[ARCHITECTURE.md](../../ARCHITECTURE.md).

## Mido and pretty_midi

### Mido

**Relationship:** Candidate integration / production utility  
**Interface:** Python  
**Typical data:** MIDI messages/files/ports

Mido is useful for low-level MIDI file and message plumbing.

Potential Prevox use:

- import/export utilities;
- validating generated MIDI;
- realtime MIDI experiments;
- translating external MIDI into Prevox-owned import DTOs.

### pretty_midi

**Relationship:** Candidate integration / reference implementation  
**Interface:** Python  
**Typical data:** MIDI → higher-level note/instrument/timing objects

pretty_midi provides a more musical view of MIDI than raw event parsing and is
useful for transformations, statistics, and preprocessing.

A useful split is:

```text
Mido        → transport/events/files
pretty_midi → note/instrument-oriented manipulation
Prevox IR   → composition semantics
```

Neither library should define Prevox's domain model.

## music21

**Relationship:** Reference implementation / candidate analysis integration  
**Interface:** Python  
**Typical data:** notes, chords, streams, scores, theory structures

music21 is relevant for:

- pitch and interval reasoning;
- chord/key analysis;
- notation and score structures;
- corpus-based analysis;
- music-theory experimentation.

It is already referenced in [REFERENCES.md](../../REFERENCES.md) because its
Stream model raises architectural questions about hierarchy and placement.

Potential Prevox use should therefore be split:

- **reference** for representation/theory concepts;
- **adapter** for optional analyses or interchange where useful.

Avoid importing music21 objects into long-lived domain types.

## MusPy

**Relationship:** Reference implementation / research tool  
**Interface:** Python

MusPy provides multiple symbolic representations and is useful for comparing
event-, note-, piano-roll-, and pitch-oriented projections.

It is also documented in [REFERENCES.md](../../REFERENCES.md) because each
representation loses different information.

## FluidSynth

**Relationship:** Candidate rendering utility / production workflow tool  
**Interface:** library / CLI  
**Typical data:** MIDI + SoundFont → audio

FluidSynth is useful for deterministic, DAW-independent preview rendering.

Potential pipeline:

```text
Prevox Music IR
      ↓
MIDI renderer
      ↓
.mid
      ↓
FluidSynth + known SoundFont
      ↓
.wav preview
```

This could support automated regression artifacts without making a particular
DAW part of Prevox's architecture.

## Rendering symbolic music

There are several different rendering paths:

- **MIDI → DAW instruments** — current human production workflow.
- **MIDI → FluidSynth/SoundFont** — predictable automated preview.
- **MIDI → plugin host** — potentially richer automated rendering; see
  [Pedalboard](audio-processing.md#pedalboard).
- **MusicXML/notation renderer** — score-oriented output.
- **live MIDI** — realtime performance/control.

These are backends. They should not change the meaning of Music IR.

## Audio-to-symbolic boundary

When [AMT](audio-transcription.md#automatic-music-transcription-amt) creates
MIDI, the result should be modeled as imported evidence rather than reconstructed
intent.

A safe conceptual path is:

```text
audio
 ↓
AMT adapter
 ↓
TranscriptionResult
  - notes
  - confidence
  - timing
  - source provenance
 ↓
explicit import/lowering step
 ↓
Music IR, if accepted
```

This preserves uncertainty instead of pretending a probabilistic model recovered
the original score or composer's intent.

## Formats to track

- **Standard MIDI File (SMF)** — performance/event interchange.
- **MIDI 2.0** — higher-resolution and per-note expression capabilities.
- **MusicXML** — score/notation interchange.
- **MEI** — richer scholarly/notation encoding.
- **SF2/SF3/SFZ** — instrument/sample definitions relevant to rendering.

MIDI 2.0, MusicXML, and MEI have direct conceptual entries in
[REFERENCES.md](../../REFERENCES.md).
