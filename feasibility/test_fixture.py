import tempfile
from pathlib import Path

from run_fixture import respond, score, seed


EXPECTED = {
    "delete_table": (False, False, False, False),
    "revoke_preserve": (True, True, True, True),
    "revoke_named": (True, False, True, False),
    "hold": (False, False, True, False),
}


def test_ground_truth_matrix():
    for policy, expected in EXPECTED.items():
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            seed(root)
            respond(root, policy)
            result = score(root, policy)
            actual = (
                result["containment_now"],
                result["durable_after_restart"],
                result["evidence_preserved"],
                result["resume_justified"],
            )
            assert actual == expected, (policy, actual, expected)


def test_missing_state_fails_closed():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        seed(root)
        (root / "credentials.json").unlink()
        result = score(root, "delete_table")
        assert result["containment_now"] is False
        assert result["durable_after_restart"] is False
        assert result["resume_justified"] is False
