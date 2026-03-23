import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "format-validator.py"
EXAMPLES = ROOT / "examples" / "expected"


class FormatValidatorCliTests(unittest.TestCase):
    def run_validator(self, format_name: str, relative_path: str) -> subprocess.CompletedProcess[str]:
        target = EXAMPLES / relative_path
        return subprocess.run(
            [sys.executable, str(SCRIPT), format_name, str(target)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_markdown_example_passes(self) -> None:
        result = self.run_validator("markdown", "checkout-tdd.md")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Validation passed.", result.stdout)

    def test_summary_example_passes(self) -> None:
        result = self.run_validator("summary", "checkout-summary.md")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_plain_text_example_passes(self) -> None:
        result = self.run_validator("plain_text", "checkout-plain-text.md")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_xray_example_passes(self) -> None:
        result = self.run_validator("xray", "checkout-xray.feature")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_zephyr_example_passes(self) -> None:
        result = self.run_validator("zephyr", "checkout-zephyr.csv")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
