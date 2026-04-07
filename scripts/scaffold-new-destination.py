#!/usr/bin/env python3
"""Create lightweight repo scaffolding for a newly researched destination."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scaffold files for a new destination format.")
    parser.add_argument("--name", required=True, help="Destination name in kebab-case")
    parser.add_argument(
        "--mode",
        choices=["artifact", "mapping"],
        default="mapping",
        help="Whether the destination is artifact-ready or mapping-only",
    )
    parser.add_argument("--root", default=".", help="Skill repository root")
    return parser


def write_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.root).resolve()
    name = args.name.strip().lower()

    reference = root / "references" / f"{name}-format.md"
    example_source = root / "examples" / "source" / f"{name}-sample.json"
    example_expected = root / "examples" / "expected" / f"{name}-sample.md"
    test_file = root / "tests" / f"test_{name}_placeholder.py"

    write_if_missing(
        reference,
        "\n".join(
            [
                f"# {name} Destination Reference",
                "",
                "Source:",
                "- Add official or primary documentation links here.",
                "",
                "Mode:",
                f"- {args.mode}",
                "",
                "Required fields:",
                "- Document destination-specific required fields here.",
                "",
                "Notes:",
                "- Record any ambiguity and constraints here.",
                "",
            ]
        ),
    )

    if args.mode == "artifact":
        template = root / "assets" / "templates" / f"{name}.j2"
        write_if_missing(
            template,
            "\n".join(
                [
                    "{# Replace this placeholder with a deterministic destination template. #}",
                    "",
                ]
            ),
        )

    write_if_missing(
        example_source,
        "{\n  \"note\": \"Replace with a researched normalized source example.\"\n}\n",
    )
    write_if_missing(
        example_expected,
        "<!-- Replace with the expected rendered artifact or mapping example. -->\n",
    )
    write_if_missing(
        test_file,
        "\n".join(
            [
                "import unittest",
                "",
                "",
                f"class {name.replace('-', ' ').title().replace(' ', '')}PlaceholderTests(unittest.TestCase):",
                "    def test_replace_me(self) -> None:",
                "        self.assertTrue(True)",
                "",
                "",
                "if __name__ == \"__main__\":",
                "    unittest.main()",
                "",
            ]
        ),
    )

    print(f"Scaffolded destination files for {name} in {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

