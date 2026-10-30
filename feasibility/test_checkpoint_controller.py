import unittest

from checkpoint_controller import CheckpointController, CheckpointProtocolError


class CheckpointControllerTests(unittest.TestCase):
    def setUp(self):
        self.official_calls = []
        self.hidden_calls = []
        self.final_calls = []

        def official(state):
            self.official_calls.append(state)
            return state["availability"]

        def hidden(state):
            self.hidden_calls.append(state)
            return state["security"]

        def final(state):
            self.final_calls.append(state)
            return {"success": state["availability"]}

        self.controller = CheckpointController(
            official_availability_oracle=official,
            hidden_security_oracle=hidden,
            final_evaluator=final,
            max_checkpoints=2,
        )

    def test_health_only_calls_both_oracles_but_hides_security(self):
        state = {"availability": True, "security": False}
        result = self.controller.checkpoint(
            state, condition="health_only", episode_open=True
        )
        self.assertEqual(result.feedback.as_agent_payload(), {"availability": "pass"})
        self.assertEqual(len(self.official_calls), 1)
        self.assertEqual(len(self.hidden_calls), 1)
        self.assertTrue(result.audit.episode_remained_open)

    def test_security_aware_returns_aggregate_bit_only(self):
        state = {"availability": True, "security": False}
        result = self.controller.checkpoint(
            state, condition="security_aware", episode_open=True
        )
        self.assertEqual(
            result.feedback.as_agent_payload(),
            {"availability": "pass", "security_invariant": "fail"},
        )
        self.assertNotIn("probe", result.feedback.message.casefold())
        self.assertFalse(result.audit.hidden_security_invariant)

    def test_checkpoint_does_not_replace_final_evaluator(self):
        state = {"availability": True, "security": False}
        self.controller.checkpoint(state, condition="health_only", episode_open=True)
        final = self.controller.finalize(state)
        self.assertEqual(final, {"success": True})
        self.assertEqual(self.final_calls, [state])

    def test_closed_episode_is_rejected(self):
        with self.assertRaises(CheckpointProtocolError):
            self.controller.checkpoint(
                {"availability": True, "security": True},
                condition="health_only",
                episode_open=False,
            )

    def test_checkpoint_budget_is_fixed(self):
        state = {"availability": True, "security": True}
        for _ in range(2):
            self.controller.checkpoint(state, condition="health_only", episode_open=True)
        with self.assertRaises(CheckpointProtocolError):
            self.controller.checkpoint(state, condition="health_only", episode_open=True)


if __name__ == "__main__":
    unittest.main()
