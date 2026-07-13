# 0008 — Keep MIDI render profiles below Music IR

- Status: Accepted
- Date: 2026-07-12

## Context

Prevox proved that a `MusicIR` value can become a usable Standard MIDI File.
The next pressure came from multi-instrument output: Logic should receive
separate lead, bass, and other parts, but Music IR must not learn MIDI tracks,
channels, programs, velocities, or instruments.

## Decision

MIDI export may accept renderer-local profiles that map logical voice
identifiers to preview output choices:

- track name;
- MIDI channel;
- preview velocity;
- General MIDI program.

These assignments belong to the MIDI backend. `Voice` remains a musical
identity, not a track or instrument.

## Consequences

- The same Music IR can be re-rendered with different arrangements.
- Logic and other DAWs can receive separate software-instrument tracks.
- MIDI program and channel choices are testable backend behavior.
- Future DAW-specific profiles can be added without changing Music IR.

## Alternatives considered

### Add instrument fields to Voice

Rejected because it would couple composition identity to one rendering
workflow.

### Emit everything on one MIDI track

Useful as a first spike, but insufficient for DAW-shaped arrangement previews.

### Introduce a canonical Performance IR now

Deferred. Renderer-local profiles are enough until multiple backends need to
share expression, articulation, or timing semantics.
