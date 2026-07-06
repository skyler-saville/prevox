# References

## Purpose

This is Prevox's annotated research notebook. It is not a list of technologies
to adopt. Each entry records an idea worth understanding, the question it raises
for Prevox, and—eventually—the result of an experiment or design decision.

Prefer specifications, papers, source repositories, and project documentation
over summaries. Record the date reviewed because software and standards change.

## Research questions

- What information belongs in Intent IR, Music IR, or neither?
- Which relationships survive useful musical transformations?
- How do existing systems represent exact time, concurrency, and repetition?
- Where do score semantics, performance semantics, and sound-control semantics
  diverge?
- Which abstractions work beyond Western common-practice notation?
- How should intent, constraints, and provenance remain inspectable?

## Intermediate representations and symbolic music

### LLVM IR

- Source: [LLVM Language Reference](https://llvm.org/docs/LangRef.html)
- Relevance: demonstrates how a shared IR lets many analyses and
  transformations operate independently of source and target.
- Prevox question: what is the smallest normalized contract on which every
  musical pass can rely?
- Status: reviewed 2026-07-06.

### MLIR

- Source: [MLIR Language Reference](https://mlir.llvm.org/docs/LangRef/)
- Relevance: supports multiple abstraction levels and progressive lowering while
  retaining graph and hierarchical structure.
- Prevox question: which invariants belong to Intent IR, which belong to Music
  IR, and what information must survive lowering between them?
- Status: reviewed 2026-07-06.

### music21 Streams

- Source: [music21 Streams user guide](https://music21.org/music21docs/usersGuide/usersGuide_04_stream1.html)
- Relevance: nested, ordered, timed containers for symbolic musical objects.
- Prevox question: which parts of hierarchical placement are useful, and where
  do flattening and shared references expose the limits of a pure tree?
- Status: reviewed 2026-07-06.

### MusPy representations

- Source: [MusPy representation documentation](https://muspy.readthedocs.io/en/stable/representations/index.html)
- Relevance: compares pitch-, piano-roll-, event-, and note-based
  representations for symbolic generation.
- Prevox question: which information each projection loses, and whether these
  should be derived views rather than canonical storage.
- Status: reviewed 2026-07-06.

### Humdrum

- Source: [Humdrum representation index](https://www.humdrum.org/Humdrum/representations.toc.html)
- Relevance: separates a general sequential syntax from many task-specific
  musical representations.
- Prevox question: should analysis annotations be independent typed layers
  rather than fields added to every IR node?
- Status: reviewed 2026-07-06.

### Allen's interval algebra

- Source: [Allen, “Maintaining Knowledge about Temporal
  Intervals”](https://cse.unl.edu/~choueiry/Documents/Allen-CACM1983.pdf)
- Relevance: represents qualitative interval relationships such as before,
  meets, overlaps, during, starts, and finishes.
- Prevox question: which small subset is musically useful in Intent IR before
  arrangement resolves exact placements?
- Status: reviewed 2026-07-06.

### Music Encoding Initiative

- Source: [MEI Guidelines](https://music-encoding.org/guidelines/dev/mei-basic/content/introduction.html)
- Relevance: distinguishes logical, visual, gestural, and analytical concerns
  in a broad music-notation encoding framework.
- Prevox question: which concerns belong in Music IR versus rendering or typed
  analytical annotations?
- Status: reviewed 2026-07-06.

## Pattern and live-coding systems

### Strudel

- Source: [Strudel pattern model](https://strudel.cc/technical-manual/patterns/)
- Relevance: models a pattern as something queried over a rational time span to
  produce events.
- Prevox question: could lazy time queries complement, but remain distinct
  from, a finite composition IR?
- Status: reviewed 2026-07-06.

### TidalCycles

- Sources: [Tidal documentation](https://tidalcycles.org/docs/),
  [pattern structure](https://tidalcycles.org/docs/reference/pattern_structure/)
- Relevance: composable pattern transformations, polymetric structure, and
  separation from sound production.
- Prevox question: which pattern combinators belong in generation and which
  imply a different time model?
- Status: reviewed 2026-07-06.

### SuperCollider Patterns

- Source: [SuperCollider Pattern Guide](https://docs.supercollider.online/Tutorials/A-Practical-Guide/PG_01_Introduction.html)
- Relevance: reusable pattern abstractions that generate event streams for a
  separate synthesis system.
- Prevox question: how should finite composition and potentially infinite
  generation use the same contracts?
- Status: queued.

### Sonic Pi

- Source: [Sonic Pi tutorial](https://sonic-pi.net/tutorial.html)
- Relevance: approachable live coding, deterministic randomization, concurrent
  loops, and code treated as an instrument.
- Prevox question: what makes algorithmic tools immediate for musicians without
  collapsing their semantics?
- Status: reviewed 2026-07-06.

### ORCΛ

- Source: [Hundred Rabbits ORCΛ repository](https://github.com/hundredrabbits/Orca-c)
- Relevance: a compact two-dimensional procedural sequencer that emits MIDI,
  OSC, and UDP rather than synthesizing sound.
- Prevox question: what does a spatial program express better than a textual or
  object API?
- Status: reviewed 2026-07-06.

### Max/MSP and Pure Data

- Sources: [Max documentation](https://docs.cycling74.com/),
  [Pure Data documentation](https://msp.ucsd.edu/Pd_documentation/index.htm)
- Relevance: mature visual dataflow environments for musical and multimedia
  systems.
- Prevox question: what graph concepts are musically legible, and which merely
  expose execution plumbing?
- Status: queued.

## Formats and interoperability

### MIDI 2.0

- Source: [The MIDI Association: MIDI 2.0](https://midi.org/midi-2-0)
- Relevance: higher-resolution messages, per-note expression, capability
  negotiation, and backward compatibility.
- Prevox question: which performance semantics deserve IR concepts and which
  remain backend-specific?
- Status: reviewed 2026-07-06.

### MusicXML 4.0

- Source: [W3C MusicXML 4.0 report](https://www.w3.org/2021/06/musicxml40/)
- Relevance: interchange for digital sheet music, including notation concepts
  absent from MIDI.
- Prevox question: how much notation intent can be derived from performance
  events, and what must be represented explicitly?
- Status: reviewed 2026-07-06.

## Generative methods and creative constraints

### Euclidean rhythms

- Source: [Toussaint, “The Euclidean Algorithm Generates Traditional Musical
  Rhythms”](https://archive.bridgesmathart.org/2005/bridges2005-47.html)
- Relevance: a small algorithm produces a broad family of maximally even
  rhythmic patterns.
- Prevox question: how should rotation, accent, meter, and cultural context be
  represented beyond a binary onset pattern?
- Status: reviewed 2026-07-06.

### Oblique Strategies

- Source: [Ableton, “Playing By The Rules: Creativity through
  constraints”](https://www.ableton.com/en/blog/creativity-through-constraints/)
- Relevance: constraints can provoke lateral creative movement rather than
  merely reject invalid work.
- Prevox question: can an intent or constraint deliberately reframe a search
  without pretending to encode taste?
- Status: queued for deeper primary-source research.

## Entry template

```markdown
### Name

- Source:
- Relevance:
- Prevox question:
- Experiment or decision:
- Status: queued | reviewed YYYY-MM-DD | superseded
```

Add an entry when a source changes a question, suggests an experiment, or warns
against a design—not merely because it mentions algorithmic music.
