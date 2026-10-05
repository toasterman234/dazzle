# Agent domain: SixB / Atlas Dazzle spike

> Audience: coding agents working on this spike.
>
> This file is a derived domain brief, not runtime authority. Source semantics remain in `toasterman234/master-repo` and the current SixB operational runtime.

## Mission

Determine whether Dazzle can faithfully model and later evaluate the existing SixB/Atlas ontology, lifecycle, policy, workflow, execution, and evidence semantics without forcing a rewrite.

## Phase 1 domain

### Work

A source-owned unit of governed work projected into SixB.

Important semantics:

- source identity must be preserved;
- canonical source state is not mutated by this spike;
- Dazzle state is initially a derived experimental projection;
- legal transitions are explicit and fail closed.

Phase 1 states:

- `ready`
- `in_progress`
- `blocked`
- `verifying`
- `done`

Minimum transitions:

- `ready -> in_progress`
- `in_progress -> blocked`
- `blocked -> in_progress`
- `in_progress -> verifying`
- `verifying -> done` only with verification evidence

`ready -> done` must not be legal.

### VerificationEvidence

Evidence that verifies the result needed to complete governed work.

Phase 1 needs only enough structure to prove that a terminal transition can require a concrete evidence reference.

## Source lineage to preserve later

D-0028 source model includes:

```
WorkProtocol
  -> WorkManifest
  -> Framework
  -> Playbook / Template

Work
  -> Lifecycle
  -> Policy / Decision / Blocker
  -> Run
  -> Evidence / VerificationEvidence

RuntimeTransition
  -> requested Work transition
  -> evaluation
  -> execution result
  -> Run/Evidence/VerificationEvidence lineage
```

The operational graph is expanding with:

```
Agent
Tool
Capability
Skill
Observation
Machine
```

## Authority rules

1. Do not treat Dazzle DSL as Atlas authority during the spike.
2. Do not change source state merely because Dazzle accepts a transition.
3. Do not invent missing relationships or semantics.
4. Record representation gaps explicitly.
5. Prefer Dazzle-native constructs where they preserve meaning.
6. Avoid side-code when DSL can express the semantics.
7. Do not use blind bootstrap/spec entity discovery as the source of truth.

## Agent workflow

Before expanding the model:

1. read the source SixB type/decision/evidence being mirrored;
2. check Dazzle's relevant stem/counter-prior/reference;
3. edit DSL in-session;
4. run `dazzle validate`;
5. run focused lint/tests;
6. read the result back;
7. document any mismatch before proceeding.

Promotion beyond Phase 1 requires verified parity on the existing SixB transition cases.
