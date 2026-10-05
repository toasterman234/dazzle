# SixB Atlas Dazzle spike

Standalone experimental Dazzle app for testing representation of the existing SixB/Atlas model.

Authority: **derived only**. SixB/master-repo remains authoritative during this spike.

## Phase 1

The first slice contains only:

- `Work`
- `VerificationEvidence`
- lifecycle transitions required to test D-0028 fit

Run from the framework checkout:

```bash
uv run dazzle validate -p spikes/sixb_atlas_dazzle
uv run dazzle lint -p spikes/sixb_atlas_dazzle
```

Do not add live SixB write-back in Phase 1.

See `../../dev_docs/2026-10-05-sixb-atlas-dazzle-spike.md` for context, source authority, plan, and promotion gates.
