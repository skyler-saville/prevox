# 0007 — Add read-only analysis passes before more generation

Status: Accepted

## Context

Prevox now has immutable domain values, deterministic transformations, and
structured diagnostics. The next compiler-engineering step is not another
mutation pass or renderer. It is analysis: pure reads over Music IR that produce
facts a future Critic, Arbiter, Composer, CLI, or GUI can inspect.

Analyses should not become Critics. A Critic interprets measurements in the
context of an Intent, style, or policy. An analysis pass simply reports what is
present in the realized music.

## Decision

Prevox introduces immutable analysis values:

- `AnalysisMetric`;
- `AnalysisReport`.

The first analysis passes are:

- `DensityAnalysis`, measuring realized note count and note density;
- `MotifReuseAnalysis`, measuring motif placement and identity reuse.

Analysis reports may include diagnostics when an analysis observes something
noteworthy, such as silent music or absent reuse. Diagnostics are not required
for every measurement.

## Consequences

- Future Critics can depend on stable measurements instead of walking Music IR
  directly.
- Golden tests can compare analysis output alongside IR output.
- Analyses provide compiler-style observability without introducing mutation,
  pass management, or musical style policy.
- The project now has the beginnings of a read-only middle-end.

## Alternatives considered

### Implement another transformation

Deferred. More transformations are useful, but analyses pressure-test traversal
and reporting without adding new mutation semantics.

### Implement Critics directly

Rejected for this slice. Critics need musical intent and preference policy.
Analyses are smaller and can feed multiple future Critics.

### Introduce a pass manager now

Deferred. There are not enough pass types yet to justify a framework. The
analysis interfaces should make a future pass manager easier without forcing
one prematurely.
