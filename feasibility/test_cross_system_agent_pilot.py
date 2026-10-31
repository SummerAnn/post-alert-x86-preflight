import json
import tempfile
import unittest
from pathlib import Path

from run_cross_system_agent_pilot import (
    CONDITIONS,
    MODELS,
    REQUIREMENT,
    SYSTEMS,
    _append_condition,
    _is_submit_command,
    _score_snapshot,
)


class CrossSystemAgentPilotTests(unittest.TestCase):
    def test_frozen_matrix_has_24_cells(self):
        self.assertEqual(len(SYSTEMS) * len(CONDITIONS) * len(MODELS) * 3, 24)

    def test_condition_only_adds_preservation_contract(self):
        text = "native task text"
        self.assertEqual(_append_condition(text, "availability_only_alert"), text)
        aware = _append_condition(text, "security_preservation_contract")
        self.assertIn(REQUIREMENT, aware)

    def test_submit_detection_is_explicit(self):
        self.assertTrue(_is_submit_command("curl -X POST http://127.0.0.1:8000/submit"))
        self.assertTrue(_is_submit_command("submit()"))
        self.assertFalse(_is_submit_command("kubectl get pods"))

    def test_independent_score_does_not_impute_missing_probe(self):
        scored = _score_snapshot(
            official_success=True,
            now={"auth_enabled": True, "role_probe": {"readWrite_geo_db": True}, "function_ok": True},
            after=None,
            probe_valid=False,
        )
        self.assertFalse(scored["independent"]["valid"])
        self.assertFalse(scored["independent"]["oracle_recovery"])


if __name__ == "__main__":
    unittest.main()
