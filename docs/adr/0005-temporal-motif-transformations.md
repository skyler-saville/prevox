# 0005 — Begin with deterministic temporal transformations

- Status: Accepted
- Date: 2026-07-06

## Context

Prevox needs a middle end that can develop musical material regardless of how
it was created. Deterministic transformations pressure-test Music IR without
introducing randomness, Composer policy, or backend behavior.

Temporal transformations are fully defined by the existing exact relative-time
model. Pitch transformations are not: transpose and inversion require decisions
about interval representation, tuning, and enharmonic spelling.

## Decision

Begin with pure Motif transformations:

- `reverse`;
- `repeat`;
- `scale_time`;
- `augment`;
- `diminish`.

Each operation:

- accepts an immutable Motif;
- requires an explicit identifier for the derived Motif;
- uses exact integer or Fraction parameters;
- returns a new Motif;
- leaves its input unchanged.

Defer transpose, invert, and mirror until pitch semantics are documented.

## Alternatives considered

### Implement all familiar transformations immediately

Rejected because semitone arithmetic would silently make 12-tone equal
temperament and a spelling policy part of Music IR.

### Give Motif mutating methods

Rejected because passes must remain composable, testable, and safe to compare.

### Reuse the source Motif identifier

Rejected because transformed material is a distinct derived value. Provenance
storage remains a later concern, but identity must not be ambiguous now.

### Add property-based testing immediately

Deferred. Algebraic invariants are first expressed as dependency-free unit
tests; a property-testing library can be justified when the input space grows.

## Consequences

- Reverse/reverse and augment/diminish invariants can be tested exactly.
- Future Composers can reuse deterministic development operations.
- Callers must deliberately name derived material.
- Pitch transformation APIs remain absent rather than misleading.
- Transformation provenance beyond source/result naming still needs a later
  design.
