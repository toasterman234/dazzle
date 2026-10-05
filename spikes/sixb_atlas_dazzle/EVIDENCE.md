# Phase 1 evidence — SixB / Atlas → Dazzle spike

Date: 2026-10-05  
Status: **Phase 1 representation/runtime proof passed; spike remains exploratory**  
Dazzle branch: `spike/sixb-atlas-dazzle-v0.1`  
Proved commit: `a9718bf1ea4e334b69b020fab48873cae51b901d`

## Authority

This evidence does **not** promote Dazzle to source of truth.

- master-repo remains authoritative for canonical definitions and lifecycle history;
- canonical `Work.state` remains source-owned;
- the Dazzle model is a derived experimental representation;
- no SixB/master-repo write-back was performed.

## Exact Mac execution boundary

All Mac execution used `toasterman234/github-workflows-control-plane` and its governed push lane.

The fork was materialized at:

`/Users/bencharney/dazzle-sixb-spike`

The proof commit was fetched by exact SHA and executed in a detached governed worktree:

`/Users/bencharney/.control-plane/worktrees/wt-a9718bf-a9d71c3e9aab`

The worktree creation result verified SHA:

`a9718bf1ea4e334b69b020fab48873cae51b901d`

Control-plane run: `37342305368`.

## Native Dazzle validation

Command:

```bash
uv run dazzle validate -p spikes/sixb_atlas_dazzle
```

Control-plane run: `37342366003`.

Result:

- dispatcher: succeeded;
- command exit code: 0;
- no parse/semantic errors.

Warnings retained intentionally for the bounded spike:

- `Work` and `VerificationEvidence` have no RBAC rules and therefore use Dazzle's backward-compatible PERMIT_UNPROTECTED behavior;
- neither entity declares `fitness.repr_fields`;
- Dazzle suggests a kanban surface because `Work` has a state machine.

These are not being papered over by inventing personas/UI/security semantics during the representation spike.

## Native Dazzle lint

The prior exact DSL commit `804bab8032ccd25b0e78aed8c89583d667bc9387` was linted with:

```bash
uv run dazzle lint -p spikes/sixb_atlas_dazzle
```

Control-plane run: `37341440129`.

Result: exit code 0.

Additional lint warnings:

- `Work` is currently a dead construct because no surface references it;
- `VerificationEvidence` is FK-referenced but has no `display_field`.

Those are expected while UI is a non-goal.

## Compiled IR read-back

The current Dazzle CLI route is:

```bash
uv run dazzle inspect project \
  --manifest spikes/sixb_atlas_dazzle/dazzle.toml \
  --entity Work \
  --format json
```

Control-plane run: `37341795897`.

Read-back proved the compiled `Work` state machine contains:

- states: `ready`, `in_progress`, `blocked`, `verifying`, `done`;
- `ready -> in_progress`;
- `in_progress -> blocked`;
- `blocked -> in_progress`;
- `in_progress -> verifying`;
- `verifying -> done`;
- the terminal transition carries exactly one guard with `requires_field = verification_evidence`;
- no `ready -> done` transition exists.

## Executable runtime proof

Committed proof:

`spikes/sixb_atlas_dazzle/scripts/prove_phase1.py`

It loads the spike's compiled AppSpec, converts the compiled state machine to the Dazzle HTTP runtime state-machine spec, and evaluates it through Dazzle's `TransitionValidator`.

Command:

```bash
uv run python spikes/sixb_atlas_dazzle/scripts/prove_phase1.py
```

Control-plane run: `37342425866`.

Authoritative output:

```json
{
  "status": "passed",
  "entity": "Work",
  "states": ["ready", "in_progress", "blocked", "verifying", "done"],
  "cases": {
    "ready_to_in_progress": "allowed",
    "ready_to_done": "rejected_invalid_transition",
    "in_progress_to_verifying": "allowed",
    "verifying_to_done_without_evidence": "rejected_guard",
    "verifying_to_done_with_evidence": "allowed"
  },
  "terminal_guard": {
    "type": "requires_field",
    "field": "verification_evidence"
  }
}
```

Exit code: 0.

## Phase 1 acceptance result

| Criterion | Result |
|---|---|
| Dazzle DSL parses/validates | PASS |
| `ready -> in_progress` | PASS — allowed |
| `ready -> done` | PASS — rejected as invalid |
| `in_progress -> verifying` | PASS — allowed |
| `verifying -> done` without evidence | PASS — rejected by guard |
| `verifying -> done` with evidence | PASS — allowed |
| source identity/provenance fields retained | PASS in DSL/compiled IR |
| source authority unchanged | PASS — no source write-back performed |

Phase 1 therefore demonstrates that Dazzle can faithfully represent and evaluate the bounded SixB lifecycle slice.

It does **not** yet prove full D-0028 parity, SixB integration, policy/RBAC parity, event lineage parity, persistence behavior, or suitability as Atlas authority.

## Control-plane findings encountered

Two request-shape failures were kept as evidence rather than treated as Dazzle failures:

1. initial validation requested `timeout_seconds=300`; the governed capability correctly rejected it because the maximum is 120;
2. an initial `dazzle inspect` attempt used the pre-v0.71.23 command shape; current Dazzle rehosts the project dumper at `dazzle inspect project`.

A separate real control-plane defect was observed repeatedly: `actions/create-github-app-token@v3` fails on the Mac runner with OpenSSL `DECODER routines::unsupported` and the workflow falls back to the runner GitHub session where allowed.

Tracked in:

`toasterman234/github-workflows-control-plane#226`

This does not invalidate the Dazzle proof, but it means the intended GitHub App authentication path is currently not healthy.

## Next gate

Do not expand automatically into the full ontology as if Dazzle were adopted.

The next exploratory slice, if continued, is to map the rest of D-0028 lineage:

`WorkProtocol -> WorkManifest -> Framework/Playbook/Template -> Work -> Lifecycle/Policy -> Run -> Evidence/VerificationEvidence -> RuntimeTransition`

and compare Dazzle evaluation against the existing SixB fixtures while preserving source ownership.


# Phase 2 evidence — D-0028 lineage + current D-0033 operational graph

Date: 2026-10-05  
Status: **Phase 2 parity proof passed; spike remains exploratory**  
Dazzle branch: `spike/sixb-atlas-dazzle-v0.1`  
Proved commit: `48d91c79c02c709394cec957f66a5606b9dbc742`

## Exact execution boundary

The exact branch head was fetched and verified in the governed Mac control plane, then executed from detached worktree:

`/Users/bencharney/.control-plane/worktrees/wt-48d91c7-55b9bc3de889`

Worktree run: `37348696757`.

## Native Dazzle validation

Command:

```bash
uv run dazzle validate -p spikes/sixb_atlas_dazzle
```

Control-plane run: `37348760478`.

Result: **PASS**, exit code 0.

The model now contains the D-0028 lineage slice plus the currently implemented D-0033 operational slice. Validation warnings remain intentionally non-blocking during this modeling spike:

- no Dazzle RBAC policy has been invented for the source-derived entities;
- no fitness `repr_fields` have been added;
- no UI/kanban/timeline surfaces are being added merely to silence capability suggestions.

## Native Dazzle lint

Command:

```bash
uv run dazzle lint -p spikes/sixb_atlas_dazzle
```

Control-plane run: `37348915110`.

Result: **PASS**, exit code 0.

Warnings are modeling/presentation guidance rather than semantic failures, including unreferenced projection/history types, missing display fields, and the intentionally broad `RuntimeTransition` record.

## D-0028 executable parity proof

Committed proof:

`spikes/sixb_atlas_dazzle/scripts/prove_phase2_d0028.py`

Fixture:

`spikes/sixb_atlas_dazzle/fixtures/d0028_parity.json`

Command:

```bash
uv run python spikes/sixb_atlas_dazzle/scripts/prove_phase2_d0028.py
```

Control-plane run: `37348978460`.

Result: **PASS**, exit code 0.

Verified:

- 15 D-0028 entities are present:
  - WorkProtocol
  - Framework
  - Playbook
  - Template
  - Lifecycle
  - LifecycleTransitionRule
  - Policy
  - Blocker
  - VerificationEvidence
  - WorkManifest
  - Work
  - Decision
  - Evidence
  - Run
  - RuntimeTransition
- all tested ref targets match the SixB source model;
- the canonical lifecycle graph matches exactly after explicit identifier normalization:
  - `in-progress -> in_progress`
  - `changes-required -> changes_required`
- native Dazzle legality matches SixB on the legal and illegal graph cases;
- the SixB missing-requirements case produces exactly:
  - `output`
  - `run-or-change-record`
- source authority remains unchanged:
  - canonical Work state is source-owned;
  - RuntimeTransition is an operational record;
  - the Dazzle projection is not authoritative.

### Explicit remaining D-0028 gap

Dazzle natively enforces the **transition graph**.

The SixB lifecycle's `requires` entries are currently transition-request inputs (for example `output`, `run-or-change-record`, `evidence`, `verifier`) rather than persistent Work fields. The spike therefore evaluates those requirements in the parity adapter instead of inventing fake Work properties solely to fit Dazzle's field-based transition guards.

This is a real integration/design question for Phase 3, not a failed parity result.

## Current D-0033 operational graph parity

Committed proof:

`spikes/sixb_atlas_dazzle/scripts/prove_phase2_d0033.py`

Fixture:

`spikes/sixb_atlas_dazzle/fixtures/d0033_graph_parity.json`

Command:

```bash
uv run python spikes/sixb_atlas_dazzle/scripts/prove_phase2_d0033.py
```

Control-plane run: `37349032427`.

Result: **PASS**, exit code 0.

Mirrored current source entities:

- Machine
- Repository
- Service
- Tool
- Capability

Verified refs:

- Service.runs_on -> Machine
- Service.defined_by -> Repository
- Tool.hosted_by -> Service
- Capability.exposed_by -> Tool
- Capability.targets -> Service

The D-0030-authorized types `Agent`, `Skill`, and `Observation` are deliberately absent because the authoritative source revision does not yet implement them as ontology types. The spike does not invent them.

The source also authorizes descriptive `Tool -> backedByProvider -> Provider` reuse, but the current Tool ontology at the proved source revision does not implement that relationship, so it is intentionally omitted here as well.

## Phase 2 acceptance result

| Criterion | Result |
|---|---|
| Latest combined DSL validates | PASS |
| Latest combined DSL lints | PASS |
| D-0028 entity/relationship parity | PASS |
| D-0028 lifecycle graph parity | PASS |
| D-0028 legal transition case | PASS |
| D-0028 illegal transition case | PASS |
| D-0028 missing-requirement case | PASS via parity adapter |
| Current D-0033 implemented graph parity | PASS |
| Unimplemented Agent/Skill/Observation invented | NO |
| Source/master-repo authority changed | NO |
| SixB write-back performed | NO |

## Phase 2 conclusion

Phase 2 is complete for the currently implemented authoritative source surface.

The spike has now proved that Dazzle can represent:

1. the governed D-0028 work/lifecycle/lineage model;
2. the currently implemented Tool/Capability/Service operational graph;
3. the lifecycle state graph using Dazzle's native runtime machinery.

It has **not** yet proved a live read-only SixB-to-Dazzle integration, persistence synchronization, API-pack compatibility, or native Dazzle enforcement of SixB's transition-request requirement payloads.

Those are Phase 3 concerns.
