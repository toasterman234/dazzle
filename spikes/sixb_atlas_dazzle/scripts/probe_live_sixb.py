#!/usr/bin/env python3
"""Read-only Phase 3 probe of the live SixB HTTP API."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_ORIGIN = os.environ.get("SIXB_API_ORIGIN", "http://127.0.0.1:3122")
WORK_ID = "work/2026-10-04-sixb-master-work-model-runtime-v0.1"


def get_json(path: str):
    url = f"{API_ORIGIN}{path}"
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def main() -> int:
    result: dict[str, object] = {
        "api_origin": API_ORIGIN,
        "mode": "read-only",
        "checks": {},
    }
    checks = result["checks"]
    assert isinstance(checks, dict)

    try:
        status, health = get_json("/health")
        checks["health"] = {"http_status": status, "body": health}

        status, ready = get_json("/ready")
        checks["ready"] = {"http_status": status, "body": ready}

        status, work_type = get_json("/api/object-types/Work")
        checks["work_type"] = {
            "http_status": status,
            "id": work_type.get("id"),
            "links": [item.get("id") for item in work_type.get("links", [])],
        }

        status, transition_type = get_json("/api/object-types/RuntimeTransition")
        checks["runtime_transition_type"] = {
            "http_status": status,
            "id": transition_type.get("id"),
            "links": [item.get("id") for item in transition_type.get("links", [])],
        }

        status, work = get_json(
            "/api/objects/Work/" + urllib.parse.quote(WORK_ID, safe="")
        )
        checks["work"] = {
            "http_status": status,
            "primary_id": work.get("primaryId"),
            "object_type_id": work.get("objectTypeId"),
            "properties": work.get("properties"),
        }

        status, transitions = get_json(
            "/api/objects?objectTypeId=RuntimeTransition&limit=200"
        )
        objects = transitions.get("objects", [])
        relevant = [
            item for item in objects
            if item.get("properties", {}).get("workId") == WORK_ID
        ]
        relevant.sort(
            key=lambda item: str(item.get("properties", {}).get("evaluatedAt", ""))
        )
        latest = relevant[-1] if relevant else None
        checks["runtime_transitions"] = {
            "http_status": status,
            "total": transitions.get("total"),
            "matching_work": len(relevant),
            "latest": latest,
        }

        result["status"] = "passed"
        print(json.dumps(result, sort_keys=True))
        return 0
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
        result["status"] = "unreachable"
        result["error"] = f"{type(exc).__name__}: {exc}"
        print(json.dumps(result, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
