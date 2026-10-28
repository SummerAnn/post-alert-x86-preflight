#!/usr/bin/env python3
"""Zero-model feasibility gate for the AIOpsLab recovery adapter.

This gate is deliberately conservative.  It only audits the checked-out
AIOpsLab source and reports whether a Kubernetes context is available.  It
does not inject faults, mutate a cluster, start a workload, or invoke a model.
The future live adapter must keep the official AIOpsLab mitigation evaluator
unchanged and add an external security oracle.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


DEFAULT_SOURCE = Path("/private/tmp/aiopslab-audit.t50o83/src")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def source_gate(source: Path) -> dict:
    files = {
        "fault_injector": source / "aiopslab/generators/fault/inject_app.py",
        "revoke_task": source / "aiopslab/orchestrator/problems/revoke_auth/revoke_auth.py",
        "tls_task": source / "aiopslab/orchestrator/problems/auth_miss_mongodb/auth_miss_mongodb.py",
        "revoke_rate": source / "aiopslab/generators/fault/script/revoke-admin-rate-mongo.sh",
        "restore_rate": source / "aiopslab/generators/fault/script/revoke-mitigate-admin-rate-mongo.sh",
        "revoke_geo": source / "aiopslab/generators/fault/script/revoke-admin-geo-mongo.sh",
        "restore_geo": source / "aiopslab/generators/fault/script/revoke-mitigate-admin-geo-mongo.sh",
    }
    missing = [str(p) for p in files.values() if not p.is_file()]
    if missing:
        return {"status": "FAIL", "missing": missing, "checks": {}}

    text = {name: read(path) for name, path in files.items()}
    role_scripts = "\n".join(
        text[name]
        for name in ("revoke_rate", "restore_rate", "revoke_geo", "restore_geo")
    )
    checks = {
        "real_role_revoke": "revokeRolesFromUser" in role_scripts,
        "real_role_restore": "grantRolesToUser" in role_scripts,
        "tls_fault": '"requireTLS"' in text["fault_injector"],
        "tls_rollback": '"disabled"' in text["fault_injector"],
        "official_mitigation_health_gate": "wait_until_pods_healthy" in text["revoke_task"]
        and "wait_until_pods_healthy" in text["tls_task"],
        "no_security_probe_in_mitigation": 'self.results["success"] = self.wait_until_pods_healthy'
        in text["revoke_task"]
        and 'self.results["success"] = self.wait_until_pods_healthy' in text["tls_task"],
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    return {"status": status, "source": str(source), "checks": checks}


def kubernetes_readiness() -> dict:
    kubectl = shutil.which("kubectl")
    if not kubectl:
        return {
            "status": "BLOCKED",
            "reason": "kubectl_not_found",
            "current_context": None,
        }
    proc = subprocess.run(
        [kubectl, "config", "current-context"],
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )
    context = proc.stdout.strip() or None
    if proc.returncode != 0 or not context:
        return {
            "status": "BLOCKED",
            "reason": "no_kubernetes_context",
            "current_context": context,
            "stderr": proc.stderr.strip()[-500:],
        }
    return {"status": "READY_TO_CHECK_CLUSTER", "current_context": context}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(os.environ.get("AIOPSLAB_SRC", DEFAULT_SOURCE)),
    )
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    source = source_gate(args.source)
    kubernetes = kubernetes_readiness()
    result = {
        "model_calls": 0,
        "mutations": 0,
        "source": source,
        "kubernetes": kubernetes,
        "overall": (
            "READY_FOR_LIVE_TRUTH_TABLE"
            if source.get("status") == "PASS" and kubernetes.get("status") == "READY_TO_CHECK_CLUSTER"
            else "BLOCKED"
        ),
    }
    encoded = json.dumps(result, indent=2, sort_keys=True)
    print(encoded)
    if args.out:
        args.out.write_text(encoded + "\n", encoding="utf-8")
    return 0 if result["overall"] == "READY_FOR_LIVE_TRUTH_TABLE" else 2


if __name__ == "__main__":
    raise SystemExit(main())

