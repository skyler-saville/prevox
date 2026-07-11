# 0002 — Use exact relative musical time

- Status: Accepted
- Date: 2026-07-06

## Context

Motifs and phrases must be reusable at different locations. Absolute bars,
wall-clock values, and MIDI ticks would couple a musical value to one placement
or backend. Floating-point beats would accumulate rounding error in tuplets and
transformations.

## Decision

Represent positions and durations as exact `fractions.Fraction` values.
Integers are accepted and converted exactly; floats are rejected.

Each `Note` has an offset relative to its Motif. Generic `Placement` values put:

- Motifs in Phrases;
- Phrases in Voices;
- Sections in Songs.

Absolute song position is a derived view formed by summing local placements.
MIDI ticks and wall-clock time remain outside Music IR.

## Alternatives considered

### Absolute song positions

Rejected because moving or repeating a phrase would require rewriting its
events.

### MIDI ticks

Rejected because transport resolution is a renderer policy.

### Floating-point beats

Rejected because they are not exact and make deterministic equality fragile.

### Leave temporal relationships unresolved in Music IR

Rejected for accepted Music IR. Relations such as `before` and `overlaps` may
exist in Intent IR, but arrangement resolves them before rendering.

## Consequences

- Reuse and local transformation are straightforward.
- Flattened timelines are projections rather than stored truth.
- Parent containers must validate that children fit.
- APIs are slightly stricter because callers must use integers or Fractions.
