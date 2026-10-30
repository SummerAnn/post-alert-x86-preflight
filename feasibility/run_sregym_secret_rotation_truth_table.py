#!/usr/bin/env python3
"""Zero-model truth table for SREGym's secret-rotation incident.

The released mitigation oracle is used unchanged for the secure arm and as a
reference for the rollback arm.  The rollback arm restores a healthy app using
the pre-rotation credential; independent probes record that the old password
remains valid and the rotated password is not the live credential.  This is a
mechanical feasibility gate, not an agent experiment.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from sregym.conductor.problems.secret_rotation_stale_env_credentials import (
    SecretRotationStaleEnvCredentialsAstronomyShop,
)


def _run_arm(arm: str) -> dict:
    problem = SecretRotationStaleEnvCredentialsAstronomyShop()
    deployed = False
    try:
        problem.app.deploy()
        deployed = True
        problem.inject_fault()
        if arm == "secure":
            problem.recover_fault()
        elif arm == "rollback":
            # Released cleanup path restores the pre-rotation credential and a
            # literal old connection string, which should make the app healthy
            # while deliberately violating the rotation invariant.
            problem._recover_to_baseline()
        else:
            raise ValueError(arm)

        official = problem.mitigation_oracle.evaluate()
        old_accepts = problem._postgres_accepts_password(problem.old_password)
        new_accepts = problem._postgres_accepts_password(problem.new_password)
        product_probe = problem.mitigation_oracle._run_product_probe()
        result = {
            "arm": arm,
            "official": official,
            "old_password_accepts": old_accepts,
            "new_password_accepts": new_accepts,
            "product_probe": product_probe,
            "old_init": problem._postgresql_init_uses_password(problem.old_password),
            "new_init": problem._postgresql_init_uses_password(problem.new_password),
            "valid": True,
        }
        return result
    finally:
        if deployed:
            try:
                problem._recover_to_baseline()
            except Exception as exc:
                print(f"cleanup warning: {exc}")
            problem.app.cleanup()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--context", default=os.environ.get("KUBE_CONTEXT", "docker-desktop"))
    args = parser.parse_args()

    # The SREGym library reads the active kubeconfig context.  Keep this gate
    # explicit so a later run cannot silently use another cluster.
    os.environ["KUBE_CONTEXT"] = args.context
    rows = [_run_arm("secure"), _run_arm("rollback")]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"all_valid": True, "rows": rows}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

