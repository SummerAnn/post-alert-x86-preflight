import unittest
from pathlib import Path

from adapter_preflight import probe_import


class AdapterPreflightTests(unittest.TestCase):
    def test_prompt_module_is_importable_without_starting_a_problem(self):
        result = probe_import(Path("/private/tmp/aiopslab-live"), "clients.utils.templates")
        self.assertTrue(result["ok"], result)

    def test_missing_module_is_reported_without_raising(self):
        result = probe_import(Path("/private/tmp/aiopslab-live"), "module_that_does_not_exist")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error_type"], "import_error")


if __name__ == "__main__":
    unittest.main()
