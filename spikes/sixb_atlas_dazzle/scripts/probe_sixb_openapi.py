#!/usr/bin/env python3
"""Probe candidate OpenAPI/documentation endpoints on the live SixB API."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

ORIGIN = "http://127.0.0.1:3122"
PATHS = [
    "/openapi.json",
    "/api/openapi.json",
    "/swagger.json",
    "/api/swagger.json",
    "/docs",
    "/api/docs",
]


def main() -> int:
    results = []
    for path in PATHS:
        url = ORIGIN + path
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                raw = response.read(4096)
                content_type = response.headers.get("content-type", "")
                entry = {
                    "path": path,
                    "status": response.status,
                    "content_type": content_type,
                    "prefix": raw.decode("utf-8", errors="replace")[:500],
                }
                if "json" in content_type.lower():
                    try:
                        parsed = json.loads(raw.decode("utf-8", errors="replace"))
                        entry["openapi"] = parsed.get("openapi") if isinstance(parsed, dict) else None
                        entry["swagger"] = parsed.get("swagger") if isinstance(parsed, dict) else None
                    except Exception:
                        pass
                results.append(entry)
        except urllib.error.HTTPError as exc:
            results.append({"path": path, "status": exc.code})
        except Exception as exc:
            results.append({"path": path, "error": f"{type(exc).__name__}: {exc}"})

    found = [
        item for item in results
        if item.get("status") == 200 and (item.get("openapi") or item.get("swagger"))
    ]
    print(json.dumps({"status":"passed","origin":ORIGIN,"openapi_found":bool(found),"results":results}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
