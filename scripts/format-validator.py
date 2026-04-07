#!/usr/bin/env python3
"""Deterministic validators for bundled test artifact formats."""

from __future__ import annotations

import argparse
import csv
import re
import sys
import zipfile
from pathlib import Path


BDD_PATTERNS = {
    "Feature": re.compile(r"^Feature:\s+\S+", re.MULTILINE),
    "Scenario": re.compile(r"^\s*Scenario(?: Outline)?:\s+\S+", re.MULTILINE),
    "Given": re.compile(r"^\s*Given\s+\S+", re.MULTILINE),
    "When": re.compile(r"^\s*When\s+\S+", re.MULTILINE),
    "Then": re.compile(r"^\s*Then\s+\S+", re.MULTILINE),
}

MARKDOWN_DETAIL_PATTERNS = {
    "Title": re.compile(r"^\*\*Title:\*\*\s+\S+", re.MULTILINE),
    "Steps": re.compile(r"^\| Step \| Action \| Expected Result \|$", re.MULTILINE),
    "Execution Type": re.compile(r"^- Execution Type:\s+\S+", re.MULTILINE),
    "Design Status": re.compile(r"^- Design Status:\s+\S+", re.MULTILINE),
}

MARKDOWN_SUMMARY_PATTERNS = {
    "Header": re.compile(r"^\| ID \| Title \| Objective \| Coverage \| Notes \|$", re.MULTILINE),
    "Separator": re.compile(r"^\|---\|---\|---\|---\|---\|$", re.MULTILINE),
}

PLAIN_TEXT_PATTERNS = {
    "Header": re.compile(
        r"^\| ID \| Path or Rule \| Preconditions \| Expected Outcome \|$",
        re.MULTILINE,
    ),
    "Separator": re.compile(r"^\|---\|---\|---\|---\|$", re.MULTILINE),
}

ZEPHYR_REQUIRED_HEADERS = [
    "Folder",
    "Name",
    "Objective",
    "Status",
    "Precondition",
    "Labels",
    "Step",
    "Expected Result",
    "Execution Type",
    "Priority",
    "Estimated Time",
    "Is Open",
]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _collect_missing(patterns: dict[str, re.Pattern[str]], text: str, label: str) -> list[str]:
    return [
        f"Missing {label} section: {section}"
        for section, pattern in patterns.items()
        if not pattern.search(text)
    ]


def validate_bdd_text(text: str) -> list[str]:
    return [f"Missing Gherkin element: {label}" for label, pattern in BDD_PATTERNS.items() if not pattern.search(text)]


def validate_markdown_detail(text: str) -> list[str]:
    return _collect_missing(MARKDOWN_DETAIL_PATTERNS, text, "markdown detail")


def validate_markdown_summary(text: str) -> list[str]:
    return _collect_missing(MARKDOWN_SUMMARY_PATTERNS, text, "markdown summary")


def validate_plain_text(text: str) -> list[str]:
    return _collect_missing(PLAIN_TEXT_PATTERNS, text, "plain-text table")


def validate_zephyr_csv(text: str) -> list[str]:
    rows = list(csv.reader(text.splitlines()))
    if not rows:
        return ["CSV content is empty"]

    header = rows[0]
    if header != ZEPHYR_REQUIRED_HEADERS:
        return ["CSV header does not match the bundled Zephyr Scale template"]

    if len(rows) < 2:
        return ["CSV must contain at least one data row"]

    non_empty_data_rows = [row for row in rows[1:] if any(cell.strip() for cell in row)]
    if not non_empty_data_rows:
        return ["CSV must contain at least one non-empty data row"]

    return []


def validate_xray_path(path: Path) -> list[str]:
    if path.suffix.lower() == ".zip":
        return validate_xray_zip(path)
    return validate_bdd_text(_read_text(path))


def validate_xray_zip(path: Path) -> list[str]:
    errors: list[str] = []
    with zipfile.ZipFile(path) as archive:
        feature_names = [name for name in archive.namelist() if name.lower().endswith(".feature")]
        if not feature_names:
            return ["ZIP must contain at least one .feature file"]

        for feature_name in feature_names:
            text = archive.read(feature_name).decode("utf-8")
            for error in validate_bdd_text(text):
                errors.append(f"{feature_name}: {error}")
    return errors


def validate(format_name: str, path: Path) -> list[str]:
    if format_name in {"markdown", "tdd"}:
        return validate_markdown_detail(_read_text(path))
    if format_name == "summary":
        return validate_markdown_summary(_read_text(path))
    if format_name == "plain_text":
        return validate_plain_text(_read_text(path))
    if format_name == "bdd":
        return validate_bdd_text(_read_text(path))
    if format_name == "xray":
        return validate_xray_path(path)
    if format_name == "zephyr":
        return validate_zephyr_csv(_read_text(path))
    return [f"Unsupported format: {format_name}"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a formatted test artifact.")
    parser.add_argument(
        "format",
        choices=["bdd", "markdown", "plain_text", "summary", "tdd", "xray", "zephyr"],
        help="Artifact format to validate",
    )
    parser.add_argument("path", help="Path to the file to validate")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"Error: file not found: {path}")
        return 1

    errors = validate(args.format, path)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
