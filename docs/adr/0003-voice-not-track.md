# 0003 — Model logical Voice rather than Track

- Status: Accepted
- Date: 2026-07-06

## Context

Tracks, channels, patches, and plugin destinations are properties of a
particular rendering workflow. If Music IR stored those concerns, the same
composition could not be freely rendered as a band, orchestra, or synth
arrangement.

The composition still needs stable identities for melodic, bass, harmonic,
pulse, and textural responsibilities.

## Decision

Music IR contains logical `Voice` values with:

- a stable identifier;
- a musical role;
- placed Phrases;
- an explicit polyphony limit.

Voice contains no instrument, MIDI track, channel, patch, or plugin.
RenderingProfile will map voices to destinations in a later milestone.

## Alternatives considered

### Track as the domain container

Rejected because the term invites transport and DAW details into composition.

### Instrument-specific parts

Deferred. Instrument capability may later be an explicit intent constraint, but
it is not the identity of a core Voice.

### Completely anonymous timelines

Rejected because Composers, Critics, and provenance need stable musical roles.

## Consequences

- Re-orchestration does not alter Music IR.
- MIDI import must infer logical voices rather than pretending tracks recover
  them.
- Polyphony is a declared musical invariant.
- Instrument-specific composition will require an explicit future design.
