# 0004 — Advance immutable CompositionState through proposals

- Status: Accepted
- Date: 2026-07-06

## Context

Context-sensitive composition needs history, but shared mutable state would make
proposal comparison, rollback, reproducibility, and local regeneration
difficult. A Composer should not change the accepted composition merely by
generating a candidate.

## Decision

`CompositionState` is an immutable revision containing:

- the currently accepted Music IR snapshot, if any;
- the sequence of AcceptanceDecisions;
- a monotonically increasing revision.

A `Proposal` contains a complete candidate Music IR in the first slice.
`CompositionState.advance()` returns a new state only when an
`AcceptanceDecision` accepts that exact Proposal.

Partial Music IR fragments and merge semantics are deferred until a real
Composer requires them.

## Alternatives considered

### Mutable shared state

Rejected because generating or evaluating a candidate could have hidden side
effects.

### Composer directly returns new state

Rejected because it would collapse creation, evaluation, and acceptance.

### Proposal contains a patch or command list

Deferred because the first manual slice does not establish suitable merge
semantics.

## Consequences

- Rejected proposals cannot alter accepted music.
- Branching and comparison can retain earlier states.
- Acceptance is auditable.
- Whole Music IR candidate snapshots may become inefficient later; a future ADR
  may introduce persistent fragments or patches when evidence demands it.
