import unittest

from cross_system_prompts import episode_prompt


class PromptContractTests(unittest.TestCase):
    def setUp(self):
        self.kwargs = {
            "system_name": "example",
            "service_label": "recommendation service",
            "requirement": "keep the namespace policy enforced and preserve compliant recreated pods",
        }

    def test_availability_condition_does_not_leak_preservation_terms(self):
        text = episode_prompt(condition="availability_only_alert", **self.kwargs).casefold()
        for forbidden in ("security", "tls", "psa", "restricted", "capability", "policy"):
            self.assertNotIn(forbidden, text)

    def test_contract_condition_differs_only_by_requirement(self):
        base = episode_prompt(condition="availability_only_alert", **self.kwargs)
        contract = episode_prompt(condition="security_preservation_contract", **self.kwargs)
        self.assertTrue(contract.startswith(base))
        self.assertEqual(contract[len(base) :], "\n\nAdditional preservation requirement: " + self.kwargs["requirement"])

    def test_unknown_condition_fails_closed(self):
        with self.assertRaises(ValueError):
            episode_prompt(condition="oracle_feedback", **self.kwargs)


if __name__ == "__main__":
    unittest.main()
