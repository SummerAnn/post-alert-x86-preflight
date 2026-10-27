"""Run the deterministic post-alert recovery fixture."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path


def seed(root: Path) -> None:
    (root / "credentials.json").write_text(
        json.dumps({"active": "cred-active", "dormant": "cred-dormant"})
    )
    (root / "signed_evidence.json").write_text(
        json.dumps({"credentials": ["cred-active", "cred-dormant"], "signed": True})
    )
    (root / "audit.log").write_text("created active and dormant credentials\n")
    (root / "service.flag").write_text("healthy\n")
    (root / "cost.json").write_text(json.dumps({"downtime_minutes": 0, "audit_events": 1}))


def respond(root: Path, policy: str) -> None:
    creds = json.loads((root / "credentials.json").read_text())
    if policy == "delete_table":
        (root / "credentials.json").unlink()
        (root / "signed_evidence.json").unlink()
        (root / "audit.log").unlink()
    elif policy == "revoke_preserve":
        creds["active"] = None
        creds["dormant"] = None
        (root / "credentials.json").write_text(json.dumps(creds))
        (root / "audit.log").open("a").write("revoked both credentials\n")
        cost = json.loads((root / "cost.json").read_text())
        cost["audit_events"] += 1
        (root / "cost.json").write_text(json.dumps(cost))
    elif policy == "revoke_named":
        creds["active"] = None
        (root / "credentials.json").write_text(json.dumps(creds))
    elif policy == "hold":
        cost = json.loads((root / "cost.json").read_text())
        cost["downtime_minutes"] = 30
        (root / "cost.json").write_text(json.dumps(cost))
        return
    else:
        raise ValueError(policy)


def score(root: Path, policy: str) -> dict[str, bool]:
    cred_path = root / "credentials.json"
    active = dormant = None
    if cred_path.exists():
        creds = json.loads(cred_path.read_text())
        active = creds.get("active") is not None
        dormant = creds.get("dormant") is not None
    evidence = False
    snapshot = root / "signed_evidence.json"
    if snapshot.exists() and (root / "audit.log").exists():
        try:
            data = json.loads(snapshot.read_text())
            evidence = data.get("signed") is True and set(data.get("credentials", [])) == {"cred-active", "cred-dormant"}
        except (ValueError, TypeError):
            evidence = False
    cost = json.loads((root / "cost.json").read_text())
    active_probe = replay_admin_request(root, "active")
    dormant_probe = replay_admin_request(root, "dormant")
    return {
        # Missing credential state is unknown, never evidence of removal.
        "containment_now": active_probe == "denied",
        "durable_after_restart": dormant_probe == "denied",
        "legitimate_function": (root / "service.flag").read_text() == "healthy\n",
        "evidence_preserved": evidence,
        "scope_reconstructable": evidence,
        "bounded_cost": cost["downtime_minutes"] <= 30 and cost["audit_events"] <= 2,
        # Closure is derived only from observed state, never from the action label.
        "resume_justified": evidence and active is False and dormant is False and cost["downtime_minutes"] <= 30,
    }


def replay_admin_request(root: Path, credential: str) -> str:
    """Simulate a fresh post-restart admin request; missing state is unknown."""
    path = root / "credentials.json"
    if not path.exists():
        return "unknown"
    creds = json.loads(path.read_text())
    if creds.get(credential):
        return "allowed"
    return "denied"


def main() -> None:
    for policy in ("delete_table", "revoke_preserve", "revoke_named", "hold"):
        with tempfile.TemporaryDirectory(prefix="post-alert- fixture-") as d:
            root = Path(d)
            seed(root)
            respond(root, policy)
            # A restart is represented by rescoring persisted state from disk.
            print(json.dumps({"policy": policy, "score": score(root, policy)}, sort_keys=True))


if __name__ == "__main__":
    main()
