module sixb_atlas.core
app sixb_atlas "SixB Atlas Dazzle Spike"

entity VerificationEvidence "Verification Evidence":
  id: uuid pk
  source_ref: str(500) required
  summary: text required
  captured_at: datetime auto_add

entity Work "Work":
  id: uuid pk
  source_id: str(200) required
  source_ref: str(500) required
  title: str(300) required
  status: enum[ready,in_progress,blocked,verifying,done]=ready
  verification_evidence: ref VerificationEvidence

  transitions:
    ready -> in_progress
    in_progress -> blocked
    blocked -> in_progress
    in_progress -> verifying
    verifying -> done: requires verification_evidence
