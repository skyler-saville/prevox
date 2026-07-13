# 0010 — Add theory and melody measurements before generation policy

- Status: Accepted
- Date: 2026-07-12

## Context

After MIDI export proved that Prevox can produce usable DAW material, the next
risk shifted from rendering to musical decision quality. Melodies, bass lines,
and drums need to relate musically before Prevox should attempt richer
generation.

However, generation policy, genre formulas, and Critics are more subjective
than measurements. The project already established that analyses are pure
facts over Music IR, while Critics interpret those facts.

## Decision

Add read-only middle-end analyses before implementing melody generation:

- tonal cohesion analysis measures scale membership and simple lead/bass
  vertical interval stability;
- melody hook analysis measures genre-neutral lead-line features such as
  repetition, range, stepwise motion, large leaps, and contour changes.

These analyses do not mutate Music IR, accept or reject proposals by
themselves, define genre profiles, or generate notes.

## Consequences

- Future Composers can make more informed melody decisions from stable metrics.
- Future Critics can interpret hook and cohesion measurements without walking
  Music IR directly.
- “Hooky” remains a tendency described by measurements, not a universal score.
- Genre remains deferred until examples justify concrete profiles.

## Alternatives considered

### Generate hook-like melodies immediately

Deferred. Without measurements first, generation would hide subjective policy
inside an algorithm.

### Add genre profiles first

Deferred. Genre profiles need measurable features to consume and compare.

### Make tonal analysis a hard validator

Rejected for now. Theory is guidance, not law; analysis reports facts and
diagnostics, while acceptance policy belongs to Critics and Arbiters.
