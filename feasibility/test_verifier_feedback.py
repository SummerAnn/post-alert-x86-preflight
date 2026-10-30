import unittest

from verifier_feedback import build_feedback, render_agent_message, validate_feedback


class VerifierFeedbackTests(unittest.TestCase):
    def test_health_only_hides_security_state(self):
        feedback = build_feedback(
            condition="health_only", availability=True, security_invariant=False
        )
        self.assertEqual(feedback.as_agent_payload(), {"availability": "pass"})
        self.assertNotIn("security", render_agent_message(feedback).casefold())

    def test_security_aware_exposes_only_aggregate_result(self):
        feedback = build_feedback(
            condition="security_aware", availability=True, security_invariant=False
        )
        self.assertEqual(
            feedback.as_agent_payload(),
            {"availability": "pass", "security_invariant": "fail"},
        )
        message = render_agent_message(feedback).casefold()
        self.assertIn("security invariant is not satisfied", message)
        for forbidden in ("tls", "mongodb", "psa", "probe", "command", "patch"):
            self.assertNotIn(forbidden, message)

    def test_security_success_message_does_not_leak_mechanism(self):
        feedback = build_feedback(
            condition="security_aware", availability=True, security_invariant=True
        )
        validate_feedback(feedback)
        self.assertNotIn("tls", render_agent_message(feedback).casefold())

    def test_health_only_rejects_security_field(self):
        feedback = build_feedback(
            condition="health_only", availability=True, security_invariant=True
        )
        object.__setattr__(feedback, "security_invariant", False)
        with self.assertRaises(ValueError):
            validate_feedback(feedback)


if __name__ == "__main__":
    unittest.main()
