# Contributing to Prevox

Prevox is still early, but it already has a shape worth protecting. Treat it
less like a MIDI toy and more like a small language implementation whose domain
happens to be music.

## Engineering principles

- Keep the domain immutable. Accepted state advances by deriving a new value,
  not by mutating an existing one.
- Keep Music IR backend-independent. MIDI tracks, channels, velocity, CC,
  plugin names, patches, and DAW concerns belong below Music IR.
- Keep logical voices separate from rendered instruments.
- Inject randomness explicitly. No hidden global random state in composers,
  transforms, analyses, renderers, or lowering passes.
- Prefer diagnostics for user-facing composition errors. Exceptions are still
  appropriate for programmer misuse and low-level invariant violations.
- Separate measurement from judgment. Analyses produce facts; Critics interpret
  facts in context.
- Add or update ADRs for architectural decisions.
- Add tests for every behavior that protects an architectural boundary.
- Add golden fixtures for new canonical traces, lowering outputs, or formatted
  compiler-style reports.

## Before changing Music IR

Music IR is the project’s most stable abstraction. A change to Music IR should
include:

1. executable evidence from an example or failing test;
2. an ADR explaining the decision and rejected alternatives;
3. updated canonical formatting or golden fixtures when observable output
   changes;
4. confirmation that MIDI/rendering concerns have not leaked upward.

If the change would only make MIDI rendering easier, it probably belongs in a
renderer, rendering profile, or future performance projection instead.

## Testing expectations

Run the full local suite before publishing work:

```bash
poetry check
poetry run python -m unittest discover -s tests -v
poetry run python -m compileall -q src tests examples
poetry run python examples/manual_trace.py > /tmp/prevox-manual-trace.txt
cmp /tmp/prevox-manual-trace.txt tests/golden/manual_trace.txt
```

The test suite includes three kinds of protection:

- unit tests for individual immutable values and pure functions;
- golden tests for canonical human-readable output;
- architectural tests for layering and long-lived invariants.

## Examples and cookbooks

Examples are part of the design process, not afterthoughts. Prefer small,
inspectable musical ideas that pressure-test the model:

- drone;
- ostinato;
- pedal tone;
- call and response;
- theme and variation;
- canon;
- rhythmic displacement.

Each mature example should eventually show the relevant intent, proposal or
manual construction, diagnostics or analyses, Music IR, and rendered output
when rendering exists.

## Pull requests

Keep PRs narrow. A good Prevox PR usually does one of these:

- adds one musical concept and its tests;
- adds one compiler-style capability and its observable output;
- records one architectural decision;
- strengthens guardrails without expanding scope.

If a PR adds an abstraction, it should also include a small musical example or
test that proves why the abstraction exists.
