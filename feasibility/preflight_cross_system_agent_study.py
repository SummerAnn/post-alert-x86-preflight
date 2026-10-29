#!/usr/bin/env python3
"""No-call preflight for the frozen cross-system agent study.

This script never contacts a model provider. It validates the frozen manifest,
provider-key presence without printing values, pinned source commits, local
Python adapters, and the disposable Kubernetes substrate.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/PREREG_CROSS_SYSTEM_AGENT_RECOVERY_2026-10-29.json"


def command(*args: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=20, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    return result.returncode == 0, (result.stdout or result.stderr).strip()


def git_head(path: Path) -> str | None:
    ok, output = command("git", "-C", str(path), "rev-parse", "HEAD")
    return output if ok else None


def main() -> int:
    errors: list[str] = []
    checks: dict[str, object] = {}

    if not MANIFEST.exists():
        errors.append(f"missing manifest: {MANIFEST}")
        print(json.dumps({"ready": False, "errors": errors}, indent=2))
        return 1

    manifest = json.loads(MANIFEST.read_text())
    checks["manifest_status"] = manifest.get("status")
    if manifest.get("status") != "frozen-before-model-calls":
        errors.append("manifest is not marked frozen-before-model-calls")
    if manifest.get("planned_model_calls") != 24:
        errors.append("planned model-call count is not 24")
    if manifest.get("repetitions_per_cell") != 3:
        errors.append("repetitions_per_cell is not 3")

    for env_name in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        checks[f"{env_name}_present"] = bool(os.environ.get(env_name))
        if not os.environ.get(env_name):
            errors.append(f"{env_name} is absent")

    for package in ("openai", "anthropic", "kubernetes", "yaml"):
        present = importlib.util.find_spec(package) is not None
        checks[f"python_{package}"] = present
        if not present:
            errors.append(f"Python package missing: {package}")

    source_commits = {
        "/private/tmp/aiopslab-live": "576c3f080c7ae2459a972afd4a2f8d5f01828430",
        "/private/tmp/SREGym": "be7dc36178c8709ddb15fb11804dadb12e1e62f4",
    }
    for raw_path, expected in source_commits.items():
        path = Path(raw_path)
        actual = git_head(path) if path.exists() else None
        checks[f"source_{path.name}"] = {"exists": path.exists(), "head": actual}
        if actual != expected:
            errors.append(f"{path} is not at pinned commit {expected}; actual={actual}")

    for required in (
        ROOT / "research/CROSS_SYSTEM_PAIRED_EVALUATOR_RESULT_2026-10-29.md",
        ROOT / "research/AIOPSLAB_LIVE_TLS_AUDIT_2026-10-28.md",
        ROOT / "research/feasibility/SREGYM_PSA_PAIRED_CONTROL_2026-10-29.md",
    ):
        checks[f"record_{required.name}"] = required.exists()
        if not required.exists():
            errors.append(f"missing prerequisite record: {required}")

    docker_ok, docker_out = command("docker", "info", "--format", "{{.ServerVersion}}")
    checks["docker"] = docker_out if docker_ok else None
    if not docker_ok:
        errors.append("Docker daemon is not available")

    kubectl_ok, kubectl_out = command("kubectl", "get", "nodes", "--no-headers")
    checks["kubectl_nodes"] = kubectl_out if kubectl_ok else None
    if not kubectl_ok or not kubectl_out:
        errors.append("kubectl has no readable node")
    elif not any(" Ready " in f" {line} " for line in kubectl_out.splitlines()):
        errors.append("no Kubernetes node is Ready")

    # Deliberately no provider request is made here.
    checks["provider_requests"] = 0
    checks["model_calls"] = 0
    result = {"ready": not errors, "checks": checks, "errors": errors}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

