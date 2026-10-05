module sixb_atlas.sixb_api

# Generated from the project-local sixb_local API pack, with only a module
# declaration added. This is a read-only external-source surface.

service sixblocal "SixB Local Runtime":
  spec: inline "pack:sixb_local"
  auth_profile: none
  # Docs: http://127.0.0.1:3122/docs

foreign_model SixbWorkObject from sixblocal "Read-only SixB Work object envelope; properties remain source-owned":
  key: primaryId
  constraint cache ttl="5"

  primaryId: str(500) required pk
  objectTypeId: str(100) required
  properties: json required

foreign_model SixbRuntimeTransitionPage from sixblocal "Read-only page envelope for current SixB RuntimeTransition objects":
  key: total
  constraint cache ttl="5"

  total: int required pk
  objects: json required

foreign_model SixbObjectType from sixblocal "Read-only SixB object-type description":
  key: id
  constraint cache ttl="30"

  id: str(100) required pk
  links: json required
