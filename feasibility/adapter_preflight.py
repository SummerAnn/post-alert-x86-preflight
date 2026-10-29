#!/usr/bin/env python3
"""No-call readiness check for the released-system agent adapters.

This is intentionally separate from the provider preflight.  It imports only
the released prompt/agent modules and reports missing runtime dependencies; it
never starts a problem, creates a namespace, contacts a model provider, or
reads independent-oracle state.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def probe_import(source_root: Path, module: str) -> dict[str, object]:
    """Import one released module in a fresh interpreter and capture only status."""
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(source_root), existing]))
    code = (
        "import importlib; importlib.import_module(" + repr(module) + ")"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "error_type": type(exc).__name__}
    if result.returncode == 0:
        return {"ok": True}
    # Keep diagnostics bounded and never include environment values.
    detail = (result.stderr or result.stdout).strip().splitlines()
    return {
        "ok": False,
        "error_type": "import_error",
        "detail": detail[-1][:240] if detail else "unknown import failure",
    }


def main() -> int:
    checks: dict[str, object] = {}
    errors: list[str] = []

    aiops = Path("/private/tmp/aiopslab-live")
    sregym = Path("/private/tmp/SREGym")
    if not aiops.exists():
        errors.append(f"missing pinned AIOpsLab checkout: {aiops}")
    if not sregym.exists():
        errors.append(f"missing pinned SREGym checkout: {sregym}")

    if aiops.exists():
        checks["aiopslab_prompt_template"] = probe_import(aiops, "clients.utils.templates")
        checks["aiopslab_agent_path"] = probe_import(aiops, "clients.react")
        checks["aiopslab_orchestrator"] = probe_import(aiops, "aiopslab.orchestrator")
        for name in ("aiopslab_agent_path", "aiopslab_orchestrator"):
            result = checks[name]
            if isinstance(result, dict) and not result.get("ok"):
                errors.append(f"{name} is not importable in the current runtime")

    if sregym.exists():
        checks["sregym_prompt_module"] = probe_import(sregym, "clients.mini_sre.mini")
        checks["sregym_conductor"] = probe_import(sregym, "sregym.conductor.conductor")
        for name in ("sregym_prompt_module", "sregym_conductor"):
            result = checks[name]
            if isinstance(result, dict) and not result.get("ok"):
                errors.append(f"{name} is not importable in the current runtime")

    checks["provider_requests"] = 0
    checks["model_calls"] = 0
    result = {"ready": not errors, "checks": checks, "errors": errors}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
