# Prevox Capabilities

This document tracks what the current architecture can express, what is under
active design pressure, and what is explicitly out of scope for now.

Status legend:

- ✅ implemented and protected by tests;
- 🚧 designed or partially explored, but not stable;
- ❌ intentionally absent;
- 🧭 future possibility, not yet committed.

## Frontend capabilities

| Capability | Status | Notes |
| --- | --- | --- |
| Python object construction | ✅ | Current examples construct Intent IR and Music IR directly. |
| Canonical human-readable inspection | ✅ | Used for the manual trace and analysis/diagnostic reports. |
| Musical Intent DSL syntax | 🚧 | Concept accepted as a future frontend; no parser or source AST yet. |
| Live coding frontend | 🧭 | Possible later frontend, not part of the current slice. |
| MIDI import | 🧭 | Planned as an importer, with explicit limits on recoverable intent. |

## Middle-end capabilities

| Capability | Status | Notes |
| --- | --- | --- |
| Intent IR distinct from Music IR | ✅ | Purpose and realization are separate semantic levels. |
| Immutable Music IR hierarchy | ✅ | Song, Section, Voice, Phrase, Motif, Note, and placement values exist. |
| Relative rational time | ✅ | Local offsets compose into derived absolute song time. |
| Logical Voice independent of instruments | ✅ | Music IR contains no track, channel, patch, plugin, or instrument assignment. |
| Deterministic temporal transformations | ✅ | Reverse, repeat, scale time, augment, and diminish Motifs. |
| Structured diagnostics | ✅ | Diagnostic values and reports exist for compiler-style workflows. |
| Read-only analyses | ✅ | Density, motif-reuse, tonal-cohesion, and melody-hook analyses return immutable reports. |
| Architectural guardrail tests | ✅ | Import layering, immutability, and Music IR field boundaries are tested. |
| Semantic tests | ✅ | Initial tests assert temporal-transform musical properties. |
| Validation passes | 🚧 | Concepts documented; only constructor invariants and diagnostics exist today. |
| Critics and arbitration behavior | 🚧 | Records exist; behavior is not implemented. |
| Transformation provenance | 🚧 | Derived identifiers exist; structured provenance is not yet modeled. |
| Pitch semantics | 🚧 | Spelled pitch values exist; interval/tuning semantics are not decided. |
| Interval semantics | 🚧 | Simple chromatic vertical interval analysis exists; transpose, invert, and mirror remain deferred. |
| Voice leading | 🚧 | Future theory/critic capability. |
| Polyphony | 🚧 | Declared voice polyphony is supported; richer polyphonic semantics are open. |
| Polymeter | ❌ | Not represented yet. |
| Microtonality | ❌ | Not represented yet. |

## Backend capabilities

| Capability | Status | Notes |
| --- | --- | --- |
| MIDI export | ✅ | Minimal deterministic Standard MIDI File writer for preview output. |
| MIDI voice profiles | ✅ | Logical voices can render as separate MIDI preview tracks, channels, velocities, and General MIDI programs without changing Music IR. |
| GM drum preview | ✅ | Temporary backend-local drum maps can render rhythm voices on MIDI channel 9; first-class percussion IR is still undecided. |
| Theory cohesion preview | ✅ | A D Dorian lead, bass, and drum example can be analyzed and exported for DAW preview. |
| Melody hook analysis | ✅ | Genre-neutral lead-line metrics measure repetition, range, stepwise motion, leaps, and contour changes. |
| MusicXML export | 🧭 | Possible later backend. |
| Logic workflow | 🧭 | Planned as a rendering/profile workflow, not a domain dependency. |
| REAPER workflow | 🧭 | Possible later backend/workflow. |
| Live MIDI stream | 🧭 | Possible later backend. |

## Next high-risk capability

The next high-risk middle-end capability is moving from analysis to informed
generation or explicit repair. Pitch representation remains the major unresolved
domain question for transpose, inversion, mirroring, voice leading, and future
non-12-TET support.
