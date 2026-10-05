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
