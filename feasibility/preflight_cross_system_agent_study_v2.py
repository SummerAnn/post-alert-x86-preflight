#!/usr/bin/env python3
"""No-call semantic preflight for the revoke-auth replacement study.

This deliberately fails closed until both released evaluator implementations
have a paired no-model control on the required substrate. It never imports a
provider SDK or makes a model request.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/PREREG_CROSS_SYSTEM_AGENT_RECOVERY_V2_2026-10-30.json"


def command(*args: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=20, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    return result.returncode == 0, (result.stdout or result.stderr).strip()


def git_head(path: Path) -> str | None:
    ok, out = command("git", "-C", str(path), "rev-parse", "HEAD")
    return out if ok else None


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="No-call preregistration and substrate preflight")
    parser.add_argument(
        "--execution-check",
        action="store_true",
        help="accept the separately recorded authorization and report execution readiness",
    )
    args = parser.parse_args()
    errors: list[str] = []
    checks: dict[str, object] = {"provider_requests": 0, "model_calls": 0}
    if not MANIFEST.exists():
        print(json.dumps({"ready": False, "errors": [f"missing {MANIFEST}"]}, indent=2))
        return 1
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("status") != "frozen-before-model-calls":
        errors.append("replacement manifest is not frozen-before-model-calls")
    authorized = manifest.get("model_calls_authorized") is True
    if authorized and not args.execution_check:
        errors.append("model_calls_authorized=true requires --execution-check")
    if args.execution_check and not authorized:
        errors.append("--execution-check requires an explicit authorization record")
    if authorized and not manifest.get("authorization_note"):
        errors.append("authorized manifest is missing authorization_note")
    if manifest.get("planned_model_calls") != 24:
        errors.append("planned_model_calls must remain 24")
    if manifest.get("repetitions_per_cell") != 3:
        errors.append("repetitions_per_cell must remain 3")

    expected = {
        "/private/tmp/aiopslab-live": "576c3f080c7ae2459a972afd4a2f8d5f01828430",
        "/private/tmp/SREGym": "be7dc36178c8709ddb15fb11804dadb12e1e62f4",
    }
    for raw, wanted in expected.items():
        path = Path(raw)
        actual = git_head(path) if path.exists() else None
        checks[f"source_{path.name}"] = {"exists": path.exists(), "head": actual}
        if actual != wanted:
            errors.append(f"{raw} is not at pinned source commit")

    # These are evidence files, never synthesized by this check.
    required_records = (
        ROOT / "research/SREGYM_REVOKE_AUTH_ZERO_MODEL_RESULT_2026-10-30.md",
        ROOT / "research/AIOPSLAB_REVOKE_AUTH_PAIRED_ZERO_MODEL_RESULT_2026-10-30.md",
    )
    for record in required_records:
        checks[f"record_{record.name}"] = record.exists()
        if not record.exists():
            errors.append(f"missing required paired-control record: {record.name}")

    adapter_record = ROOT / "research/ADAPTER_DRY_RUN_2026-10-30.md"
    checks[f"record_{adapter_record.name}"] = adapter_record.exists()
    if not adapter_record.exists():
        errors.append("missing required adapter dry-run record")

    checks["OPENAI_API_KEY_present"] = bool(os.environ.get("OPENAI_API_KEY"))
    checks["ANTHROPIC_API_KEY_present"] = bool(os.environ.get("ANTHROPIC_API_KEY"))
    docker_ok, docker_out = command("docker", "info", "--format", "{{.ServerVersion}}")
    checks["docker"] = docker_out if docker_ok else None
    if not docker_ok:
        errors.append("Docker daemon is not available")
    kubectl_ok, kubectl_out = command("kubectl", "get", "nodes", "--no-headers")
    checks["kubectl_nodes"] = kubectl_out if kubectl_ok else None
    if not kubectl_ok or not kubectl_out:
        errors.append("kubectl has no readable node")
    checks["status"] = "ready_for_model_pilot" if authorized else "ready_for_pinned_x86_adapter_dry_run"
    print(json.dumps({"ready": not errors, "checks": checks, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

