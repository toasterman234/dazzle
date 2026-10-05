module sixb_atlas.core
app sixb_atlas "SixB Atlas Dazzle Spike"

# Phase 2 remains a derived experimental projection of master-repo/SixB.
# Dazzle identifiers cannot contain hyphens, so canonical lifecycle tokens
# in-progress and changes-required normalize to in_progress and changes_required.
# source_state / LifecycleTransitionRule retain the canonical tokens explicitly.

entity WorkProtocol "Work Protocol":
  id: uuid pk
  source_id: str(500) required unique
  title: str(300) required
  status: str(100)
  version: str(100) required
  source_ref: str(800) required
  content_hash: str(128) required
  provenance: str(500)
  observed_at: datetime

entity Framework "Framework":
  id: uuid pk
  source_id: str(500) required unique
  title: str(300) required
  status: str(100)
  version: str(100) required
  source_ref: str(800) required
  content_hash: str(128) required
  provenance: str(500)
  observed_at: datetime

entity Playbook "Playbook":
  id: uuid pk
  source_id: str(500) required unique
  title: str(300) required
  status: str(100)
  version: str(100)
  source_ref: str(800) required
  content_hash: str(128)
  provenance: str(500)
  observed_at: datetime

entity Template "Template":
  id: uuid pk
  source_id: str(500) required unique
  title: str(300) required
  status: str(100)
  version: str(100) required
  source_ref: str(800) required
  content_hash: str(128) required
  provenance: str(500)
  observed_at: datetime

entity Lifecycle "Lifecycle":
  id: uuid pk
  source_id: str(500) required unique
  title: str(300) required
  version: str(100) required
  states_json: text required
  transitions_json: text required
  rules_json: text required
  source_ref: str(800) required
  content_hash: str(128) required
  provenance: str(500)
  observed_at: datetime

entity LifecycleTransitionRule "Lifecycle Transition Rule":
  id: uuid pk
  lifecycle: ref Lifecycle required
  from_state: str(100) required
  to_state: str(100) required
  normalized_from_state: str(100) required
  normalized_to_state: str(100) required
  requirements_json: text required
  source_ref: str(800) required

entity Policy "Policy":
  id: uuid pk
  source_id: str(500) required unique
  title: str(300) required
  effect: str(100) required
  scope: text required
  source_ref: str(800) required
  provenance: str(500)

entity Blocker "Blocker":
  id: uuid pk
  source_id: str(500) required unique
  title: str(300) required
  state: str(100) required
  source_ref: str(800) required
  provenance: str(500)
  observed_at: datetime

entity VerificationEvidence "Verification Evidence":
  id: uuid pk
  source_id: str(500) required unique
  kind: str(100) required
  summary: text required
  captured_at: datetime required
  source_ref: str(800) required
  provenance: str(500)

entity WorkManifest "Work Manifest":
  id: uuid pk
  source_id: str(500) required unique
  title: str(300) required
  status: str(100) required
  source_ref: str(800) required
  source_version: str(100) required
  content_hash: str(128) required
  provenance: str(500)
  initialized_by: ref WorkProtocol required
  selects_framework: ref Framework required
  selects_playbook: ref Playbook required
  instantiated_from: ref Template required
  lifecycle: ref Lifecycle required

entity Work "Work":
  id: uuid pk
  source_id: str(500) required unique
  title: str(300) required
  kind: str(100) required
  source_state: str(100) required
  status: enum[proposed,ready,in_progress,verification,accepted,changes_required,blocked,closed]=ready
  source_ref: str(800) required
  provenance: str(500)
  observed_at: datetime required
  described_by: ref WorkManifest
  governed_by_lifecycle: ref Lifecycle required
  governing_policy: ref Policy
  blocker: ref Blocker

  transitions:
    proposed -> ready
    ready -> in_progress
    in_progress -> verification
    in_progress -> blocked
    verification -> accepted
    verification -> changes_required
    verification -> blocked
    changes_required -> in_progress
    accepted -> closed

entity Decision "Decision":
  id: uuid pk
  source_id: str(500) required unique
  title: str(300) required
  status: str(100) required
  decided_at: datetime
  source_ref: str(800) required
  provenance: str(500)
  observed_at: datetime required
  authorizes: ref Work required

entity Evidence "Evidence":
  id: uuid pk
  source_id: str(500) required unique
  kind: str(100) required
  summary: text required
  captured_at: datetime required
  source_ref: str(800) required
  provenance: str(500)
  evidences: ref Work required

entity Run "Run":
  id: uuid pk
  source_id: str(500) required unique
  kind: str(100) required
  status: str(100) required
  started_at: datetime required
  finished_at: datetime
  source_ref: str(800) required
  provenance: str(500)
  run_of: ref Work required
  used_manifest: ref WorkManifest required
  initialized_by: ref WorkProtocol required
  used_framework: ref Framework required
  followed: ref Playbook required
  instantiated_from: ref Template required
  produced_evidence: ref Evidence
  verification_evidence: ref VerificationEvidence

entity RuntimeTransition "Runtime Transition":
  id: uuid pk
  source_id: str(500) required unique
  work_id: str(500) required
  from_state: str(100) required
  to_state: str(100) required
  status: str(100) required
  legal: bool required
  evaluation_reason: text required
  missing_requirements_json: text required
  requested_at: datetime required
  evaluated_at: datetime required
  executed_at: datetime
  source_ref: str(800) required
  provenance: str(500)
  for_work: ref Work required
  produced_run: ref Run
  produced_evidence: ref Evidence
  verified_by: ref VerificationEvidence
