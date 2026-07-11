## Summary

<!-- What changed, and why? -->

## Architectural checklist

- [ ] Added or updated an ADR if this changes architecture.
- [ ] Added or updated golden output if canonical formatting or lowering output changed.
- [ ] Added semantic or architectural tests when preserving a property matters.
- [ ] Updated `LLM_CONTEXT.md` if project state, risks, or workflow changed.
- [ ] Documentation matches implementation.
- [ ] Domain and Music IR remain independent of backends, MIDI, DAWs, and rendering profiles.
- [ ] Randomness, if any, is explicit and reproducible.
- [ ] User-facing errors use diagnostics where appropriate.

## Validation

<!-- Include relevant commands, usually:

poetry check
poetry run python -m unittest discover -s tests -v
poetry run python -m compileall -q src tests examples
poetry run python examples/manual_trace.py > /tmp/prevox-manual-trace.txt && cmp /tmp/prevox-manual-trace.txt tests/golden/manual_trace.txt

-->
