import unittest

from action_trace_contract import record_turn, serialize_turn


class ActionTraceContractTests(unittest.TestCase):
    def test_preserves_exact_model_text_and_action(self):
        raw = "Thought: inspect the deployment\nAction: kubectl get pods -n hotel-reservation"
        turn = record_turn(0, raw, "kubectl get pods -n hotel-reservation")
        self.assertEqual(serialize_turn(turn), {
            "turn_index": 0,
            "raw_response": raw,
            "parsed_action": "kubectl get pods -n hotel-reservation",
            "parse_status": "parsed",
        })

    def test_ambiguous_or_missing_action_is_a_void(self):
        turn = record_turn(1, "I should investigate first.", None)
        self.assertEqual(turn.parse_status, "void_missing_or_ambiguous_action")
        self.assertIsNone(serialize_turn(turn)["parsed_action"])

    def test_invalid_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            record_turn(-1, "x", None)
        with self.assertRaises(TypeError):
            record_turn(0, b"x", None)
        with self.assertRaises(ValueError):
            record_turn(0, "x", "  ")


if __name__ == "__main__":
    unittest.main()
