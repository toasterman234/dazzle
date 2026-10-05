module sixb_atlas.sixb_api

# Derived from the project-local sixb_local API pack. The current API-pack
# generator/parser disagree on foreign constraint syntax, so this spike omits
# optional constraints. Read-only is enforced by GET-only pack operations and
# foreign_model semantics; no SixB mutation operation is declared.

service sixblocal "SixB Local Runtime":
  spec: inline "pack:sixb_local"
  auth_profile: none
  # Docs: http://127.0.0.1:3122/docs

foreign_model SixbWorkObject from sixblocal "Read-only SixB Work object envelope; properties remain source-owned":
  key: primaryId
  primaryId: str(500) required pk
  objectTypeId: str(100) required
  properties: json required

foreign_model SixbRuntimeTransitionPage from sixblocal "Read-only page envelope for current SixB RuntimeTransition objects":
  key: total
  total: int required pk
  objects: json required

foreign_model SixbObjectType from sixblocal "Read-only SixB object-type description":
  key: id
  id: str(100) required pk
  links: json required
