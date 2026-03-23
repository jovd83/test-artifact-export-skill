import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "render-artifact.py"
SOURCE = ROOT / "examples" / "source" / "checkout-cases.json"
EXPECTED = ROOT / "examples" / "expected"


class RenderArtifactCliTests(unittest.TestCase):
    def render(self, format_name: str, suffix: str) -> tuple[subprocess.CompletedProcess[str], Path]:
        temp_dir = Path(tempfile.mkdtemp())
        output_path = temp_dir / f"artifact{suffix}"
        result = subprocess.run(
            [sys.executable, str(SCRIPT), format_name, str(SOURCE), str(output_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        return result, output_path

    def test_render_markdown_matches_expected(self) -> None:
        result, output_path = self.render("markdown", ".md")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(output_path.read_text(encoding="utf-8"), (EXPECTED / "checkout-tdd.md").read_text(encoding="utf-8"))

    def test_render_summary_matches_expected(self) -> None:
        result, output_path = self.render("summary", ".md")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(output_path.read_text(encoding="utf-8"), (EXPECTED / "checkout-summary.md").read_text(encoding="utf-8"))

    def test_render_plain_text_matches_expected(self) -> None:
        result, output_path = self.render("plain_text", ".md")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(output_path.read_text(encoding="utf-8"), (EXPECTED / "checkout-plain-text.md").read_text(encoding="utf-8"))

    def test_render_xray_matches_expected(self) -> None:
        result, output_path = self.render("xray", ".feature")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(output_path.read_text(encoding="utf-8"), (EXPECTED / "checkout-xray.feature").read_text(encoding="utf-8"))

    def test_render_zephyr_matches_expected_rows(self) -> None:
        result, output_path = self.render("zephyr", ".csv")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        actual_rows = list(csv.reader(output_path.read_text(encoding="utf-8").splitlines()))
        expected_rows = list(csv.reader((EXPECTED / "checkout-zephyr.csv").read_text(encoding="utf-8").splitlines()))
        self.assertEqual(actual_rows, expected_rows)


if __name__ == "__main__":
    unittest.main()
