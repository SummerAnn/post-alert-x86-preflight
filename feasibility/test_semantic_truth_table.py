import unittest
from pathlib import Path

from validate_semantic_truth_table import validate


class SemanticTruthTableTests(unittest.TestCase):
    def test_recorded_sregym_table_fails_the_preregistered_known_good_gate(self):
        path = (
            Path(__file__).resolve().parents[1]
            / "research/feasibility/SREGYM_CHECKPOINT_TRUTH_TABLE_2026-10-30.json"
        )
        ok, errors = validate(path)
        self.assertFalse(ok)
        self.assertIn("known_good security invariant is not pass", errors)


if __name__ == "__main__":
    unittest.main()
