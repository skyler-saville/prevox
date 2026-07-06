# Roadmap

## Delivery strategy

Each phase should end in a playable or inspectable vertical slice. New
abstractions are introduced by working features, not by filling an anticipated
directory tree.

## Phase 0 — Language and boundaries

**Outcome:** the project has a stable reason to exist and a shared vocabulary.

- agree on the vision, non-goals, and human collaboration loop;
- record the philosophy used to settle future tradeoffs;
- define dependency direction and bounded contexts;
- define the roles, shapes, and lowering boundary of Intent IR and Music IR;
- define immutable `CompositionState` and proposal-based state transitions;
- define local rational time, relational intent time, and derived absolute
  views;
- separate logical voices from rendering assignments;
- define minimal `Critique` and `AcceptanceDecision` semantics;
- test the initial grammar against small hand-written musical examples;
- establish an annotated research notebook;
- distinguish Intent IR from the later Musical Intent DSL syntax;
- record architectural decisions as they become expensive to reverse.

**Exit criteria**

- the foundation documents are internally consistent;
- both IRs are distinguished from source ASTs and backend formats;
- Intent IR can express question, answer, escalation, resolution, and target
  curves without containing notes;
- Music IR can retain provenance back to the intent and decision that produced
  it;
- Music IR uses relative local placement and contains no MIDI ticks or
  instrument assignments;
- MIDI and DAW concepts do not leak into the domain;
- each initial object has one clear responsibility;
- one melody, one chordal passage, one drum pattern, and one reused motif can be
  represented on paper without untyped escape hatches;
- deferred features are explicitly named.

## Phase 0.5 — IR playground

**Outcome:** both representations can be read and challenged before MIDI hides
their weaknesses.

- build a minimal console or notebook inspector;
- hand-construct an eight-bar Intent IR plan in D Dorian;
- represent phrase roles, a reused motif, and a rising energy curve;
- realize the plan into Music IR with one deliberately simple melody composer;
- print Intent IR, Music IR, and the lowering decisions between them;
- print each proposal's rationale, independent critiques, and acceptance reason;
- keep the implementation small enough to replace when the model is wrong.

**Exit criteria**

- the intent tree makes compositional sense without notes;
- the realized tree makes musical sense without MIDI;
- each realized phrase and event can be traced to intent and an actual decision;
- one deterministic Critic can disagree with a Composer's predicted effect;
- a RenderingProfile can assign a logical voice without changing Music IR;
- changing one phrase intent does not perturb unrelated material;
- inspecting the models reveals more than printing Python object internals.

Example inspection:

```text
CompositionPlan: D Dorian, 8 bars
└── SectionIntent: verse
    ├── PhraseIntent: question, energy 0.3, motif A
    ├── PhraseIntent: answer, energy 0.5, vary motif A
    └── PhraseIntent: escalation, energy 0.7, introduce motif B

Proposal: answer-02
├── Reason: answer motif A while increasing motion
├── Predicted effect: energy +0.20 (confidence 0.76)
├── IntentCritic: measured +0.12 (confidence 0.91)
└── Decision: accepted by baseline-policy-v1

Song
└── Section: verse @ +0
    └── Voice: lead
        └── Phrase: answer-02 @ +2 bars
            ├── Motif: A, variation
            ├── Note @ +0 beats
            └── Note @ +1/2 beat

RenderingProfile
└── Voice lead → preview instrument
```

## Phase 1 — Core composition slice

**Outcome:** Prevox deterministically composes eight bars of monophonic melody
in D Dorian and represents the result as Music IR.

- stabilize only the IR concepts proven in the playground;
- implement exact musical time, pitch, note, scale, and chord values;
- implement relative `Placement`, `Motif`, `Phrase`, `Voice`, `Section`, and
  `Song`;
- implement stable identity, references, and minimal provenance;
- define minimal `Composer`, `Generator`, `Constraint`, and `Transformer`
  protocols only where the slice exercises them;
- define minimal `Critic`, `Critique`, `Arbiter`, and `AcceptanceDecision`
  contracts exercised by the slice;
- implement immutable `CompositionState`, `Proposal`, and acceptance;
- inject seeded randomness and derive stable child seeds;
- provide hierarchical and flattened timeline traversal;
- test invariants, placement, reuse, equality, and deterministic generation.

Start with only the vocabulary listed in `MUSICAL_GRAMMAR.md`. Avoid persistence,
frameworks, and abstract plugin machinery.

**Exit criteria**

- the same seed and inputs produce identical domain events;
- a simple melody composer realizes phrase intent from composition state;
- a phrase can be placed, repeated, and transformed without mutation;
- derived absolute positions equal the composition of local placements;
- one motif can be referenced by multiple phrases with visible lineage;
- a song containing at least one eight-bar phrase can be constructed;
- the domain test suite performs no filesystem or MIDI I/O.

## Phase 2 — MIDI interoperability

**Outcome:** Music IR crosses the DAW boundary through dedicated adapters.

### 2A: Export

- map beat positions and durations to MIDI ticks;
- map logical voices through an explicit RenderingProfile;
- export tempo, meter, tracks, note-on, and note-off events;
- define deterministic ordering for simultaneous events;
- open the exported file in Logic Pro or another DAW and listen.

**Exit criteria**

- an eight-bar generated song exports to `test.mid`;
- it plays at the expected tempo, rhythm, pitch, and duration;
- repeated exports are musically equivalent and deterministically encoded;
- MIDI details remain confined to the adapter;
- changing the assigned instrument or channel does not change Music IR.

### 2B: Import

- import notes, tempo, meter, and useful track metadata;
- quantize only by explicit policy;
- report information that MIDI cannot recover;
- verify export → import equivalence at the event-model level.

**Exit criteria**

- a supported MIDI file becomes valid domain material;
- a Prevox MIDI round trip preserves defined musical properties;
- import never invents motif, intent, or provenance without labeling inference.

## Phase 3 — A small generator library

**Outcome:** musicians can compare genuinely different idea-making strategies.

- random-walk melody;
- Euclidean rhythm;
- first-order Markov melody or harmony;
- integrate each primitive through a context-sensitive composer;
- allow at least two proposals for one intent and select through Critics and an
  Arbiter;
- shared composition state and deterministic seed handling;
- generator-specific parameters without a universal “options” dictionary.

**Exit criteria**

- each generator has a narrow algorithm-specific contract;
- composers turn generator candidates into valid Music IR proposals;
- proposal rationales and Critiques remain distinguishable in provenance;
- same seed means same result and changed seeds produce useful variation;
- algorithms can be tested without MIDI;
- at least one example combines two generators in a song.

## Phase 4 — Theory, transformations, and Intent DSL

**Outcome:** material can be evaluated and developed in musically meaningful
ways.

- add transpose, reverse, invert, repeat, quantize, and humanize transforms as
  demand warrants;
- validate scale membership, range, interval limits, rhythmic consistency,
  resolution, and basic voice leading;
- implement focused Theory, Motif, Rhythm, and Novelty Critics as demonstrated
  by examples;
- expand the initial Intent IR dimensions into qualitative profiles and
  weighted constraints;
- introduce an intent source AST only if a textual syntax is actually adopted;
- support time-varying intent such as “build energy over eight bars”;
- preserve selected motif features through transformation.

**Exit criteria**

- validation explains violations without silently changing material;
- repairs are explicit transformations;
- compiled intent is inspectable and versioned;
- intent lowers to or operates on Music IR without adding backend concepts;
- examples demonstrate `tense`, `building`, `sparse`, and `preserve motif`;
- measurements show whether generated output met the requested intent;
- arbitration retains critic disagreement rather than only a total score.

## Phase 5 — Logic template workflow

**Outcome:** generated voices land predictably in an existing production
template.

- define export-track naming conventions;
- map voices to instruments, channels, or template destinations through a
  Logic-specific RenderingProfile;
- document a repeatable Logic import workflow;
- preserve the generic MIDI path.

**Exit criteria**

- one command produces a MIDI artifact that aligns with a documented template;
- the same song still exports without Logic-specific configuration;
- no Logic concept enters the domain model.

## Phase 6 — Visual composition

**Outcome:** a GUI or graph editor exposes the established application model.

- validate user workflows before choosing graph, timeline, or hybrid editing;
- visualize generation, transformation, and provenance relationships;
- allow local regeneration and comparison of variations;
- keep all composition behavior available through application use cases.

**Exit criteria**

- users can build and revise a small composition without editing Python;
- the interface explains intent compilation and validation feedback;
- UI state is not the canonical composition format.

## Later, only with evidence

- plugin hosting and third-party lifecycle;
- AI-assisted generators;
- learned human-preference and LLM Critics;
- Strudel and live-coding integration;
- real-time MIDI;
- MusicXML;
- headless audio/plugin rendering;
- evolutionary and constraint-solving research.

These are candidate adapters or algorithms, not assumptions the core must carry
today.

## First audible checkpoint

The first end-to-end target remains intentionally small:

```python
plan = CompositionPlan(key="D Dorian", bars=8)
plan.add(PhraseIntent(role="question"))
plan.add(PhraseIntent(role="answer"))

music = compose(plan, seed=48291)
MidiRenderer(profile="gm-preview").write(music, "test.mid")
```

The checkpoint is complete when the same seed produces the same eight bars of
monophonic D Dorian melody in Logic. Before that, phase 0.5 must make both IRs
and their lowering decisions intelligible in the console. The API spelling may
evolve; the user-visible loop should remain this simple.
