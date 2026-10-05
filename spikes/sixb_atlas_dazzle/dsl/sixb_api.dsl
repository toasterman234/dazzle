module sixb_atlas.sixb_api

# Derived from the project-local sixb_local API pack. Current Dazzle API-pack
# generation emits legacy `constraint cache`; the active parser accepts
# read_only/event_driven/batch_import, so this live bridge uses `read_only`.

service sixblocal "SixB Local Runtime":
  spec: inline "pack:sixb_local"
  auth_profile: none
  # Docs: http://127.0.0.1:3122/docs

foreign_model SixbWorkObject from sixblocal "Read-only SixB Work object envelope; properties remain source-owned":
  key: primaryId
  constraint read_only

  primaryId: str(500) required pk
  objectTypeId: str(100) required
  properties: json required

foreign_model SixbRuntimeTransitionPage from sixblocal "Read-only page envelope for current SixB RuntimeTransition objects":
  key: total
  constraint read_only

  total: int required pk
  objects: json required

foreign_model SixbObjectType from sixblocal "Read-only SixB object-type description":
  key: id
  constraint read_only

  id: str(100) required pk
  links: json required
