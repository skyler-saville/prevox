# Project Comparison Framework

[← Ecosystem index](README.md)

This framework keeps project research useful for architecture and product
positioning rather than becoming a list of software names.

Use it for Frayed Banner projects and for external projects worth comparing
against them.

## Core questions

Every substantial project comparison should answer:

1. **What problem does this solve?**
2. **What is the closest existing project or product?**
3. **Where do the projects overlap?**
4. **Where are their architectural boundaries different?**
5. **What is the best use case where this project is the better fit?**

Also record:

- **Primary representation** — intent, symbolic music, MIDI, waveform audio,
  plugin graph, score, model tensor, etc.
- **Primary user** — composer, performer, producer, developer, mastering
  engineer, researcher, or listener.
- **Input/output contract** — what enters and leaves the system?
- **Ownership** — Frayed Banner, external open source, external commercial,
  standard/specification, or research.
- **Relationship** — dependency, candidate integration, reference
  implementation, adjacent project, production workflow tool, research only,
  or watchlist.
- **Maintenance** — active, mature/stable, experimental, archived, or unknown.
- **License** — and whether it creates distribution constraints.
- **Best use cases** — concrete workflows, not generic marketing descriptions.
- **Poor-fit use cases** — important boundaries the project should resist.
- **Architectural consequence** — whether this comparison changes a port,
  domain boundary, roadmap item, ADR, or nothing.

## Comparison rule

Do not compare projects only by feature count.

Two tools can both "generate music" while solving very different problems.
Likewise, two mastering systems can produce similar outputs while differing
substantially in transparency, automation model, and integration surface.

Prefer comparisons based on the same problem space, different abstraction, and
different best use case.

## Canonical project summary

A project page should contain:

- a short definition;
- the problem it solves;
- its core model;
- best use cases;
- poor-fit use cases;
- closest comparisons;
- relationship to other Frayed Banner projects;
- architecture implications;
- research status and review date.

## Comparison maintenance

Comparisons age faster than architectural definitions.

When reviewing a comparison:

- re-check whether the external project is still maintained;
- verify that its license has not changed;
- distinguish a project's current released behavior from experimental branches;
- update the review date;
- avoid treating popularity or GitHub stars as evidence of technical fit;
- prefer primary documentation and source repositories.

## Why this belongs in the ecosystem catalog

The comparison layer answers a different question from Prevox's
[capabilities](../capabilities.md) or architectural
[references](../../REFERENCES.md):

- **Capabilities:** what Prevox can do.
- **References:** what changed an architectural question.
- **Ecosystem comparisons:** what exists around us, how it differs, and when it
  is the better tool.

This distinction should remain when the ecosystem material eventually moves to
a dedicated Frayed Banner knowledge repository.
