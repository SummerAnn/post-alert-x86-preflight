#!/usr/bin/env python3
"""Deterministically summarize completed cross-system pilot cells.

This script never imputes a missing/void cell and never writes a scientific
verdict.  It is intentionally a descriptive report over immutable per-cell
JSON records emitted by ``run_cross_system_agent_pilot.py``.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


EXPECTED = 24


def _rows(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(root.glob("**/rep_*.json")):
        try:
            row = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            rows.append({"path": str(path), "status": "void_malformed", "error": str(exc)})
            continue
        row["path"] = str(path)
        rows.append(row)
    return rows


def _success(row: dict[str, Any], key: str) -> bool:
    if key == "official":
        return bool((row.get("official_result") or {}).get("success") is True)
    if key == "independent":
        return bool((row.get("independent") or {}).get("oracle_recovery") is True)
    if key == "security_now":
        return bool(((row.get("security_now") or {}).get("role_probe") or {}).get("readWrite_geo_db"))
    if key == "security_after":
        return bool(((row.get("security_after_fresh_process") or {}).get("readWrite_geo_db")))
    raise KeyError(key)


def summarize(root: Path) -> dict[str, Any]:
    rows = _rows(root)
    complete = [r for r in rows if r.get("status") == "complete"]
    void = [r for r in rows if r.get("status") != "complete"]
    grouped: dict[str, dict[str, Any]] = defaultdict(lambda: {"cells": 0, "complete": 0, "void": 0})
    for row in rows:
        key = "|".join(str(row.get(k, "?")) for k in ("system", "condition", "requested_model"))
        out = grouped[key]
        out["cells"] += 1
        if row.get("status") == "complete":
            out["complete"] += 1
            for metric in ("official", "independent", "security_now", "security_after"):
                out[metric] = out.get(metric, 0) + int(_success(row, metric))
        else:
            out["void"] += 1
    return {
        "expected_cells": EXPECTED,
        "observed_cell_files": len(rows),
        "complete_cells": len(complete),
        "void_or_malformed_cells": len(void),
        "missing_cells": max(0, EXPECTED - len(rows)),
        "groups": dict(sorted(grouped.items())),
        "void_paths": [r.get("path") for r in void],
        "provider_requests": sum(int(r.get("provider_requests", 0) or 0) for r in rows),
        "resolved_models": sorted({r.get("resolved_model") for r in rows if r.get("resolved_model")}),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = summarize(args.root)
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
