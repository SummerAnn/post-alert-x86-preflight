#!/usr/bin/env python3
"""Fail-closed semantic validator for recorded mechanical control tables.

This validator is intentionally separate from the checkpoint wrapper's
payload-consistency flag. It never starts a cluster, contacts a provider, or
modifies the recorded JSON.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate(path: Path) -> tuple[bool, list[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = {str(row.get("arm")): row for row in data.get("rows", [])}
    errors: list[str] = []
    for required in ("known_good", "secure_repair", "rollback"):
        if required not in rows:
            errors.append(f"missing semantic arm: {required}")

    if not errors:
        known = rows["known_good"]
        secure = rows["secure_repair"]
        rollback = rows["rollback"]
        if known.get("official_success") is not True:
            errors.append("known_good official availability is not pass")
        if known.get("security_state", {}).get("security_invariant") is not True:
            errors.append("known_good security invariant is not pass")
        if secure.get("official_success") is not True:
            errors.append("secure_repair official availability is not pass")
        if secure.get("security_state", {}).get("security_invariant") is not True:
            errors.append("secure_repair security invariant is not pass")
        if rollback.get("security_state", {}).get("security_invariant") is not False:
            errors.append("rollback security invariant is not fail")

    return not errors, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    ok, errors = validate(args.path)
    print(json.dumps({"semantic_gate": "pass" if ok else "fail", "errors": errors}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
