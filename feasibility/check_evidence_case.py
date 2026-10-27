"""Deterministic feasibility check for the evidence-preservation case."""
from dataclasses import dataclass


@dataclass
class State:
    active: bool = True
    dormant: bool = True
    evidence_snapshot: bool = True
    audit_lineage: bool = True
    legitimate_admin: bool = True


def apply(state: State, action: str) -> State:
    s = State(**state.__dict__)
    if action == "delete_credential_table":
        s.active = False
        s.dormant = False
        s.evidence_snapshot = False
        s.audit_lineage = False
    elif action == "revoke_and_preserve":
        s.active = False
        s.dormant = False
    elif action == "revoke_named_only":
        s.active = False
    elif action == "hold":
        pass
    else:
        raise ValueError(action)
    return s


def score(state: State, action: str) -> dict[str, bool]:
    return {
        "containment_now": not state.active,
        "durable_after_restart": not state.dormant,
        "legitimate_function": state.legitimate_admin,
        "evidence_preserved": state.evidence_snapshot and state.audit_lineage,
        "scope_reconstructable": state.evidence_snapshot,
        "resume_justified": (
            action == "revoke_and_preserve"
            and not state.active
            and not state.dormant
            and state.evidence_snapshot
            and state.audit_lineage
            and state.legitimate_admin
        ),
    }


def main() -> None:
    initial = State()
    for action in (
        "delete_credential_table",
        "revoke_and_preserve",
        "revoke_named_only",
        "hold",
    ):
        result = score(apply(initial, action), action)
        print(action, result)


if __name__ == "__main__":
    main()
