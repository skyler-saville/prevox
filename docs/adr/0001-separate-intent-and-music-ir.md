# 0001 — Separate Intent IR and Music IR

- Status: Accepted
- Date: 2026-07-06

## Context

Prevox must represent both unresolved compositional purpose and realized
symbolic music. Combining them would either force intent into note-shaped
objects or require renderers to interpret goals such as “escalate” and
“resolve.”

A source AST would preserve the syntax of one frontend, while Prevox may have
Python builders, a future DSL, importers, and algorithmic Composers.

## Decision

Use two canonical semantic levels:

- Intent IR represents rhetorical role, duration, targets, constraints, and
  preservation.
- Music IR represents realized songs, sections, logical voices, phrases,
  motifs, notes, and placements.

The first implementation exposes immutable `Intent` and `MusicIR` roots. A
Proposal links one Intent identifier to one candidate Music IR.

## Alternatives considered

### One combined domain tree

Rejected because unresolved goals and realized notes have different invariants
and lifecycles.

### Only Music IR

Rejected because intent would become informal metadata and could not be
validated or inspected independently.

### Treat the future DSL AST as Intent IR

Rejected because normalized intent semantics must not depend on one source
syntax.

## Consequences

- Intent can be inspected before notes exist.
- Imported Music IR may legitimately have unknown intent.
- Lowering from intent to music becomes an explicit, traceable operation.
- Cross-IR provenance is required.
- The two models must remain small enough that their separation does not become
  ceremonial mapping.
