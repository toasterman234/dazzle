#!/usr/bin/env python3
"""Phase 3 proof: Dazzle-native local API pack over the live SixB runtime."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

from dazzle.api_kb.loader import load_pack, set_pack_project_root


ROOT = Path(__file__).resolve().parents[1]
WORK_ID = "work/2026-10-04-sixb-master-work-model-runtime-v0.1"


def get_json(url: str):
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def main() -> None:
    set_pack_project_root(ROOT)
    pack = load_pack("sixb_local")
    assert pack is not None, "project-local sixb_local API pack was not discovered"
    assert pack.base_url == "http://127.0.0.1:3122"
    assert pack.auth is not None and pack.auth.auth_type == "none"
    assert pack.operations, "pack must declare operations"
    assert all(op.method == "GET" for op in pack.operations), "pack must remain GET-only"

    operations = {op.name: op for op in pack.operations}
    assert {
        "get_sixb_work_object",
        "list_sixb_runtime_transition_page",
        "get_sixb_work_type",
        "get_sixb_runtime_transition_type",
    } <= set(operations)

    service_dsl = pack.generate_service_dsl()
    foreign_dsl = [pack.generate_foreign_model_dsl(model) for model in pack.foreign_models]

    assert 'spec: inline "pack:sixb_local"' in service_dsl
    assert "auth_profile: none" in service_dsl
    generated_foreign_dsl = "\n".join(foreign_dsl)
    assert "foreign_model SixbWorkObject" in generated_foreign_dsl
    assert "foreign_model SixbRuntimeTransitionPage" in generated_foreign_dsl
    assert "constraint cache" not in generated_foreign_dsl, (
        "current parser rejects legacy API-pack cache constraints"
    )

    committed_api_dsl = (ROOT / "dsl" / "sixb_api.dsl").read_text()
    assert "constraint cache" not in committed_api_dsl
    assert "constraint read_only" not in committed_api_dsl, (
        "current lexer rejects read_only in foreign constraint position; "
        "read-only is enforced by foreign_model ownership plus GET-only operations"
    )
    assert committed_api_dsl.count("foreign_model ") == 3

    work_path = operations["get_sixb_work_object"].path.replace(
        "{id}", urllib.parse.quote(WORK_ID, safe="")
    )
    status, work = get_json(pack.base_url + work_path)
    assert status == 200
    assert work["primaryId"] == WORK_ID
    assert work["objectTypeId"] == "Work"
    assert work["properties"]["state"] == "in-progress"

    status, transitions = get_json(
        pack.base_url + operations["list_sixb_runtime_transition_page"].path
    )
    assert status == 200
    assert "objects" in transitions and "total" in transitions

    status, work_type = get_json(pack.base_url + operations["get_sixb_work_type"].path)
    assert status == 200
    assert work_type["id"] == "Work"

    status, transition_type = get_json(
        pack.base_url + operations["get_sixb_runtime_transition_type"].path
    )
    assert status == 200
    assert transition_type["id"] == "RuntimeTransition"

    result = {
        "status": "passed",
        "pack": {
            "name": pack.name,
            "provider": pack.provider,
            "base_url": pack.base_url,
            "auth": pack.auth.auth_type,
            "operations": [
                {"name": op.name, "method": op.method, "path": op.path}
                for op in pack.operations
            ],
            "foreign_models": [model.name for model in pack.foreign_models],
        },
        "live": {
            "work_primary_id": work["primaryId"],
            "work_state": work["properties"]["state"],
            "runtime_transition_total": transitions["total"],
            "work_type_id": work_type["id"],
            "runtime_transition_type_id": transition_type["id"],
        },
        "generated": {
            "service_dsl": service_dsl,
            "foreign_model_dsl": foreign_dsl,
        },
        "authority": {
            "get_only": True,
            "dazzle_projection_authoritative": False,
            "sixb_write_back": False,
        },
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
