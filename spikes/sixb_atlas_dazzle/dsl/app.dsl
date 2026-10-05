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
  lifecycle_ref: ref Lifecycle required
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
  policy_scope: text required
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
  record_kind: str(100) required
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
  lifecycle_ref: ref Lifecycle required

entity Work "Work":
  id: uuid pk
  source_id: str(500) required unique
  title: str(300) required
  record_kind: str(100) required
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
  record_kind: str(100) required
  summary: text required
  captured_at: datetime required
  source_ref: str(800) required
  provenance: str(500)
  evidences: ref Work required

entity Run "Run":
  id: uuid pk
  source_id: str(500) required unique
  record_kind: str(100) required
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

# Current operational graph slice from authoritative master-repo @
# 64e19ec47bdd2a1197ee7caaed4c1c0499488d5a.
# D-0033 currently implements Tool + Capability over Service. Agent / Skill /
# Observation are authorized by D-0030 but do not yet exist as ontology types
# in this source revision, so this spike deliberately does not invent them.

entity Machine "Machine":
  id: uuid pk
  source_id: str(500) required unique
  hostname: str(300) required
  os_name: str(200) required
  architecture: str(100) required
  source_ref: str(800) required
  provenance: str(500)
  observed_at: datetime required

entity Repository "Repository":
  id: uuid pk
  source_id: str(500) required unique
  full_name: str(500) required
  profile: str(200)
  status: str(100)
  head_sha: str(128)
  source_ref: str(800) required
  provenance: str(500)
  observed_at: datetime required

entity Service "Service":
  id: uuid pk
  source_id: str(500) required unique
  name: str(300) required
  record_kind: str(100) required
  status: str(100) required
  origins: text
  source_ref: str(800) required
  provenance: str(500)
  observed_at: datetime required
  runs_on: ref Machine
  defined_by: ref Repository

entity Tool "Tool":
  id: uuid pk
  source_id: str(500) required unique
  name: str(300) required
  record_kind: str(100) required
  endpoint: str(1000)
  source_ref: str(800) required
  provenance: str(500)
  observed_at: datetime required
  hosted_by: ref Service

entity Capability "Capability":
  id: uuid pk
  source_id: str(500) required unique
  name: str(300) required
  integration: str(300) required
  owner: str(500) required
  provider_name: str(300)
  identity_label: str(500)
  last_health_status: str(100)
  last_health_checked_at: datetime
  status: str(100) required
  source_ref: str(800) required
  provenance: str(500)
  observed_at: datetime required
  exposed_by: ref Tool required
  targets: ref Service

# Explicit Phase 3 UI shell.
# Public because this local personal spike has auth disabled in dazzle.toml.
# This avoids relying on Dazzle's implicit/generated workspace selection.

surface atlas_work_list "Work":
  uses entity Work
  mode: list
  section main:
    field title "Title"
    field source_state "Canonical State"
    field status "Dazzle State"
    field record_kind "Kind"
    field observed_at "Observed"
    field source_ref "Source"

surface atlas_transition_list "Runtime Transitions":
  uses entity RuntimeTransition
  mode: list
  section main:
    field work_id "Work"
    field from_state "From"
    field to_state "To"
    field status "Status"
    field legal "Legal"
    field evaluation_reason "Reason"
    field evaluated_at "Evaluated"

surface atlas_evidence_list "Evidence":
  uses entity Evidence
  mode: list
  section main:
    field record_kind "Kind"
    field summary "Summary"
    field captured_at "Captured"
    field source_ref "Source"

surface atlas_tool_list "Tools":
  uses entity Tool
  mode: list
  section main:
    field name "Name"
    field record_kind "Kind"
    field endpoint "Endpoint"
    field observed_at "Observed"

surface atlas_capability_list "Capabilities":
  uses entity Capability
  mode: list
  section main:
    field name "Name"
    field integration "Integration"
    field provider_name "Provider"
    field status "Status"
    field last_health_status "Health"
    field observed_at "Observed"

surface atlas_service_list "Services":
  uses entity Service
  mode: list
  section main:
    field name "Name"
    field record_kind "Kind"
    field status "Status"
    field observed_at "Observed"

workspace atlas_home "Atlas":
  purpose: "Public local dashboard for the SixB / Atlas Dazzle spike"
  access: public
  stage: "command_center"

  work_board:
    source: Work
    display: kanban
    group_by: status
    empty: "No projected Work records are in Dazzle yet."

  transitions:
    source: RuntimeTransition
    display: list
    sort: evaluated_at desc
    limit: 20
    empty: "No RuntimeTransition records are in Dazzle yet."

  evidence:
    source: Evidence
    display: list
    sort: captured_at desc
    limit: 20
    empty: "No Evidence records are in Dazzle yet."

  tools:
    source: Tool
    display: grid
    sort: name asc
    empty: "No Tool records are in Dazzle yet."

  capabilities:
    source: Capability
    display: list
    sort: name asc
    empty: "No Capability records are in Dazzle yet."

  services:
    source: Service
    display: list
    sort: name asc
    empty: "No Service records are in Dazzle yet."

