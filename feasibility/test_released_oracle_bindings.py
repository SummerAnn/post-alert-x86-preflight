import unittest

from released_oracle_bindings import aiopslab_availability_checkpoint, sregym_availability_checkpoint


class ReleasedOracleBindingTests(unittest.TestCase):
    def test_aiopslab_binding_calls_health_helper_without_submit(self):
        class Task:
            namespace = "demo"

            def __init__(self):
                self.calls = []

            def wait_until_pods_healthy(self, namespace, timeout=None):
                self.calls.append((namespace, timeout))
                return True

            def submit(self):
                raise AssertionError("submit must not be called by checkpoint")

        task = Task()
        self.assertTrue(aiopslab_availability_checkpoint(task, timeout=0))
        self.assertEqual(task.calls, [("demo", 0)])

    def test_sregym_binding_reads_only_official_success_bit(self):
        class Oracle:
            def __init__(self):
                self.calls = 0

            def evaluate(self):
                self.calls += 1
                return {"success": True, "ignored_diagnostic": "not exposed"}

        oracle = Oracle()
        self.assertTrue(sregym_availability_checkpoint(oracle))
        self.assertEqual(oracle.calls, 1)

    def test_malformed_results_fail_closed(self):
        class BadOracle:
            def evaluate(self):
                return {"success": "yes"}

        with self.assertRaises(RuntimeError):
            sregym_availability_checkpoint(BadOracle())


if __name__ == "__main__":
    unittest.main()
