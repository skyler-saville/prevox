# 0009 — Treat GM drums as a backend-local preview policy

- Status: Accepted
- Date: 2026-07-12

## Context

The first multi-voice MIDI output handled pitched lead and bass parts. Drums
are different in General MIDI: drum kit pieces are selected by note number on
MIDI channel 10, not by ordinary pitched semantics.

Prevox does not yet have a first-class percussion event in Music IR.

## Decision

Support a temporary General MIDI drum preview inside the MIDI backend:

- drum output uses mido channel `9`, corresponding to MIDI channel 10;
- selected symbolic pitches are mapped to GM drum note numbers;
- binary `.mid` artifacts remain generated and ignored;
- first-class percussion IR remains deferred.

The current preview convention is intentionally narrow and documented as a
renderer policy, not a theory model.

## Consequences

- Logic can import generated drum MIDI as a separate playable software
  instrument.
- Music IR still contains no channel, kit, pad, or instrument assignment.
- VS Code MIDI preview plugins may not sound authoritative for drum timbre;
  Logic import is the current DAW proving ground.
- A future percussion model can replace this policy when examples require
  percussion semantics that analysis, transformation, or generation must
  understand.

## Alternatives considered

### Treat drum pitches as normal melody pitches

Rejected as a permanent model because “kick” and “snare” are not pitch classes.

### Add `PercussionHit` immediately

Deferred because the current need is export preview, not domain-level
percussion transformation or analysis.

### Make drums Logic-specific

Rejected. The preview uses standard MIDI/GM behavior first; Logic-specific
workflow can be layered later.
