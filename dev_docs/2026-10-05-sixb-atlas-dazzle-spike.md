# SixB / Atlas → Dazzle spike

Status: exploratory
Date: 2026-10-05
Branch: `spike/sixb-atlas-dazzle-v0.1`

## Goal

Test whether Dazzle can represent and evaluate the existing SixB/Atlas domain and lifecycle model cleanly enough to become a candidate semantic/governance runtime beside SixB.

This is **not** an adoption or authority transfer. The spike stays derived and reversible.

## Existing source system

Authoritative source material currently lives in `toasterman234/master-repo`, especially:

- `experiments/sixb-operational-runtime-v0.1/`
- `docs/decisions/D-0028-sixb-master-work-model-runtime-v0.1.md`
- `docs/work/2026-10-04-sixb-master-work-model-runtime-v0.1.md`
- `experiments/sixb-operational-runtime-v0.1/docs/EVIDENCE.md`
- D-0030 / EXP-0020 Agent–Tool operational graph work

The current SixB work-model slice includes or authorizes:

- Work
- WorkProtocol
- WorkManifest
- Framework
- Template
- Playbook
- Lifecycle
- Blocker
- Policy
- Decision
- Run
- Evidence
- VerificationEvidence
- RuntimeTransition

The expanding operational graph also includes:

- Agent
- Tool
- Capability
- Skill
- Observation
- relationships to Machine / Work / Playbook / Run / Evidence

## Existing authority boundary that must be preserved

Current D-0028 semantics are deliberate:

- canonical master-repo definitions remain source-owned;
- canonical `Work.state` remains source-owned;
- SixB may evaluate/execute a requested transition and record the result;
- `RuntimeTransition` is SixB-owned request/evaluation/execution lineage;
- runtime execution must not silently mutate/reset canonical Work state;
- successful transition attempts produce Run/Evidence/VerificationEvidence lineage;
- missing requirements and illegal transitions fail closed.

A Dazzle spike must not erase this distinction.

## Why Dazzle is being tested

Dazzle provides first-class:

- entities and relationships;
- state transitions with requirements/guards;
- processes/workflows;
- permissions and scope rules;
- event semantics;
- services/integrations and foreign models;
- runtime API/UI generated from DSL;
- agent-oriented project tooling;
- portable agent skills;
- MCP tooling;
- domain cognition via `dazzle domain`;
- DSL validation/linting.

### Supported creation/agent paths relevant to this spike

1. `dazzle init` blank project.
2. `dazzle init --from <example>`.
3. Direct coding-agent edits to DSL followed by `dazzle validate`.
4. `dazzle agent sync` portable project-local skills/workflows.
5. Dazzle MCP guidance/tooling for an in-session agent.
6. `dazzle domain extract|show|gaps|research|promote`.
7. `AGENT_DOMAIN.md` as the agent-facing domain intermediate.
8. `SPEC.md` as requirements input.
9. Existing example apps as pattern/reference sources.
10. API-pack/OpenAPI tooling for a later live SixB integration.

Dazzle's own current counter-prior says not to trust bootstrap/analyze-spec/discover_entities as the primary prose→DSL authoring path. Preferred shape is grounded domain brief → domain cognition → in-session agent authors DSL → validate.

## Chosen spike shape

```
master-repo / SixB
       |
       | read only / grounded source
       v
AGENT_DOMAIN.md
       |
       | in-session agent + Dazzle knowledge/skills
       v
Dazzle DSL
       |
       v
dazzle validate / lint
       |
       v
standalone experimental Dazzle runtime
```

No SixB write-back is part of Phase 1.

## Phase 1 — smallest useful proof

Mirror only:

- Work
- VerificationEvidence
- transition semantics needed to prove lifecycle fit

Required behavior:

1. `ready -> in_progress` is legal.
2. `ready -> done` is not declared/legal.
3. `in_progress -> verifying` is legal.
4. `verifying -> done` requires VerificationEvidence.
5. source identity/provenance are retained.
6. the project clearly labels its Work state as a derived experimental projection.

### Phase 1 acceptance

- Dazzle DSL parses/validates.
- Transition shape is faithful to source intent.
- Illegal/missing-requirement behavior is explicit.
- No source authority is changed.
- Gaps/mismatches are documented instead of papered over.

## Phase 2 — only after Phase 1 is verified

Add the remaining D-0028 model:

- WorkProtocol
- WorkManifest
- Framework
- Template
- Playbook
- Lifecycle
- Blocker
- Policy
- Decision
- Run
- Evidence
- RuntimeTransition

Then add the D-0030 operational graph:

- Agent
- Tool
- Capability
- Skill
- Observation

Then compare Dazzle evaluation against the same fixtures used by the existing SixB proof.

## Phase 3 — optional live connection

Only if parity is good:

- expose/read SixB API/OpenAPI;
- evaluate `dazzle api-pack scaffold` / `generate-dsl`;
- create read-only foreign models/services or a thin adapter;
- keep source ownership explicit;
- separately decide whether Dazzle is evaluator-only, domain authority, or merely a useful modeling surface.

## Non-goals

- rewriting SixB;
- making this fork authoritative for Atlas;
- copying every object immediately;
- creating a new universal event store;
- adding external writes;
- changing Dazzle framework internals unless a real blocker is demonstrated.

## Evidence sources consulted before starting

- Dazzle root `AGENTS.md`
- Dazzle project tracker example and transition syntax
- Dazzle domain/agent workflow docs and counter-prior
- SixB D-0028 work/decision/evidence
- current SixB `RuntimeTransition` implementation/evidence
- current Agent/Tool operational graph work

## Current state

Phase 1 and Phase 2 are now **verified** under `spikes/sixb_atlas_dazzle/`.

Evidence is recorded in `spikes/sixb_atlas_dazzle/EVIDENCE.md`.

### Phase 1

The bounded lifecycle mechanism proof passed using Dazzle's native runtime validator.

### Phase 2

The latest proved Dazzle commit is:

`48d91c79c02c709394cec957f66a5606b9dbc742`

Verified on the governed Mac runner:

- native `dazzle validate`: exit 0;
- native `dazzle lint`: exit 0;
- D-0028 entity/relationship/lifecycle parity proof: PASS;
- D-0033 current operational graph parity proof: PASS.

The D-0028 model now includes the full tested lineage slice:

`WorkProtocol -> WorkManifest -> Framework/Playbook/Template -> Work -> Lifecycle/Policy/Blocker -> Decision/Run -> Evidence/VerificationEvidence -> RuntimeTransition`

The canonical lifecycle is represented exactly after explicit DSL-safe token normalization:

- `in-progress -> in_progress`
- `changes-required -> changes_required`

The currently implemented D-0033 source surface is also mirrored:

`Machine -> Service <- Tool <- Capability` plus `Repository -> Service` definition provenance.

`Agent`, `Skill`, and `Observation` are **not** invented because the authoritative source revision has not yet implemented them as ontology types.

One real design gap is now explicit: Dazzle natively validates transition graph legality, while SixB's lifecycle `requires` entries are transition-request inputs rather than persistent Work fields. Phase 2 evaluates those requirements in the parity adapter instead of creating fake fields.

The spike remains exploratory. No SixB/master-repo authority was transferred and no source write-back was performed.

### Next gate — Phase 3

Phase 3 may now explore a **read-only live connection**:

1. use the existing loopback SixB API (`/api/objects`, `/api/object-types`) as the source surface;
2. determine whether Dazzle's API-pack/OpenAPI path applies; current SixB proof code exposes REST endpoints but no project-local OpenAPI artifact has been identified yet;
3. if API-pack cannot consume SixB directly, build only a thin read-only adapter/foreign-model bridge;
4. prove live read-back of Work + RuntimeTransition first;
5. do not add SixB write-back or authority mutation.

No adoption decision is implied by entering Phase 3.

### Phase 3 current status

The live GET-only SixB connection has been proved and the project-local Dazzle API pack is implemented. No machine-readable OpenAPI document is exposed at the tested SixB paths, so the spike uses a bounded local API pack with read-only foreign models.

The latest source also corrects a Dazzle API-pack generator/parser mismatch: generated legacy `constraint cache` is not accepted by the current parser, so this bridge uses native `constraint read_only` and removes local cache TTL metadata.

Phase 3 is not yet accepted because the final fresh validation pass hit Mac disk exhaustion while uv was creating another temporary-worktree environment. This is an execution-environment blocker, not a semantic failure.

The next action is strictly cleanup of control-plane-owned Dazzle verification worktrees, followed by one fresh validate/lint/live API-pack proof. No write-back or authority change is permitted.

