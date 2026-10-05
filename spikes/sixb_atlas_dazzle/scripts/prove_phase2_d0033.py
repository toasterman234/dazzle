#!/usr/bin/env python3
"""Phase 2 current operational graph parity proof (D-0033 source revision)."""

from __future__ import annotations

import json
from pathlib import Path

from dazzle.cli.utils import load_project_appspec


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "d0033_graph_parity.json"


def field_map(entity):
    return {field.name: field for field in entity.fields}


def main() -> None:
    fixture = json.loads(FIXTURE.read_text())
    appspec = load_project_appspec(ROOT)
    entities = {entity.name: entity for entity in appspec.domain.entities}

    for name in fixture["mirrored_entities"]:
        assert name in entities, f"missing mirrored entity: {name}"

    checked: dict[str, dict[str, str]] = {}
    for entity_name, expected in fixture["expected_refs"].items():
        fields = field_map(entities[entity_name])
        checked[entity_name] = {}
        for field_name, target in expected.items():
            assert field_name in fields, f"{entity_name}.{field_name} missing"
            actual = fields[field_name].type.ref_entity
            assert actual == target, f"{entity_name}.{field_name}: {actual} != {target}"
            checked[entity_name][field_name] = actual

    # Do not invent authorized-but-unimplemented ontology types.
    absent = []
    for name in fixture["authorized_but_not_implemented_in_source"]:
        if name not in entities:
            absent.append(name)
    assert sorted(absent) == sorted(fixture["authorized_but_not_implemented_in_source"])

    # Presence of graph objects must remain descriptive, never an execution grant.
    assert fixture["authority"]["materialization_grants_execution_authority"] is False
    assert fixture["authority"]["dazzle_projection_authoritative"] is False

    result = {
        "status": "passed",
        "source": fixture["source"],
        "mirrored_entities": fixture["mirrored_entities"],
        "implemented_d0030_types": fixture["implemented_d0030_types"],
        "relationship_refs_checked": checked,
        "authorized_but_not_implemented_omitted": absent,
        "authority": fixture["authority"],
        "omissions": fixture["omissions"],
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
