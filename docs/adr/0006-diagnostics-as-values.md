# 0006 — Represent user-facing failures as diagnostics

Status: Accepted

## Context

As Prevox becomes more compiler-like, invalid musical input should be reported
as inspectable feedback rather than only as Python exceptions. A future DSL,
project file, pass manager, or CLI will need to show several problems at once:
where they occurred, what was expected, and whether they block acceptance.

The core value objects still enforce programmer-facing invariants with normal
Python exceptions. Those constructors are not a parser or user-input boundary.

## Decision

Prevox introduces immutable diagnostic values:

- `DiagnosticSeverity`;
- `DiagnosticLocation`;
- `Diagnostic`;
- `DiagnosticReport`.

Compiler-like steps may return a `DiagnosticReport` before attempting an
operation. The first concrete use is transform preflight checks for Motif
operations such as repeat, time scaling, augmentation, and diminution.

Diagnostic locations use domain paths such as `Song → Section → Motif` because
Prevox does not yet have stable source files or spans. Source spans can be
added later without replacing domain-path locations.

## Consequences

- Future passes, validators, frontends, and renderers have a shared diagnostic
  vocabulary.
- Tests can assert readable compiler output instead of matching exception text.
- Domain constructors remain compact and strict while user-facing workflows can
  accumulate multiple errors.
- Diagnostic codes become observable behavior and should change deliberately.

## Alternatives considered

### Exceptions only

Rejected for user-facing compiler workflows. Exceptions are still appropriate
for internal invariant violations, but they do not provide enough structure for
pipeline reports, golden tests, or multiple simultaneous errors.

### Full source-span diagnostics immediately

Deferred. There is no parser or persistence format yet, so source spans would be
speculative. Domain-path locations are useful now and compose with future source
locations.

### Pass manager first

Deferred. Diagnostics are a smaller primitive and can support transforms,
validators, and eventual passes without forcing a pass-management framework
before enough passes exist.
