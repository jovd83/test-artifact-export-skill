#!/usr/bin/env python3
"""Render bundled destinations from a normalized JSON source."""

from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def render_markdown_detail(data: dict) -> str:
    test_case = data["test_cases"][0]
    lines = [f"### {test_case.get('id', test_case['title'])}", "", f"**Title:** {test_case['title']}", ""]
    if test_case.get("description"):
        lines.extend([f"**Description:** {test_case['description']}", ""])
    traceability = test_case.get("requirements_coverage", [])
    if traceability:
        lines.append("**Traceability**")
        lines.extend(f"- {item}" for item in traceability)
        lines.append("")
    preconditions = test_case.get("preconditions", [])
    if preconditions:
        lines.append("**Preconditions**")
        lines.extend(f"{index}. {item}" for index, item in enumerate(preconditions, start=1))
        lines.append("")
    lines.extend(
        [
            "**Steps**",
            "",
            "| Step | Action | Expected Result |",
            "|---|---|---|",
        ]
    )
    for index, step in enumerate(test_case.get("steps", []), start=1):
        lines.append(f"| {index} | {step.get('action', '')} | {step.get('expected_result', '')} |")
    lines.extend(
        [
            "",
            "**Metadata**",
            "",
            f"- Execution Type: {test_case.get('execution_type', 'Manual')}",
            f"- Design Status: {test_case.get('design_status', 'Draft')}",
        ]
    )
    optional_metadata = [
        ("Test Suite", "test_suite"),
        ("Test Level", "test_level"),
        ("Test Engineer", "test_engineer"),
        ("Notes", "notes"),
    ]
    for label, field in optional_metadata:
        if test_case.get(field):
            lines.append(f"- {label}: {test_case[field]}")
    return "\n".join(lines).rstrip() + "\n"


def render_summary(data: dict) -> str:
    lines = [
        "| ID | Title | Objective | Coverage | Notes |",
        "|---|---|---|---|---|",
    ]
    for test_case in data.get("test_cases", []):
        lines.append(
            f"| {test_case.get('id', '')} | {test_case['title']} | {test_case.get('objective', '')} | "
            f"{test_case.get('coverage', '')} | {test_case.get('notes', '')} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def render_plain_text(data: dict) -> str:
    lines = [
        "| ID | Path or Rule | Preconditions | Expected Outcome |",
        "|---|---|---|---|",
    ]
    for test_case in data.get("test_cases", []):
        preconditions = "; ".join(test_case.get("preconditions", []))
        lines.append(
            f"| {test_case.get('id', '')} | {test_case['title']} | {preconditions} | {test_case.get('expected_outcome', '')} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def render_bdd(data: dict) -> str:
    lines: list[str] = []
    for tag in data.get("feature_tags", []):
        lines.append(f"@{tag}")
    lines.extend(
        [
            f"Feature: {data['feature_title']}",
            f"  As a {data['persona']}",
            f"  I want {data['behavior']}",
            f"  So that {data['value']}",
            "",
        ]
    )
    background = data.get("background", [])
    if background:
        lines.append("  Background:")
        lines.extend(f"    {step}" for step in background)
        lines.append("")
    for scenario in data.get("scenarios", []):
        for tag in scenario.get("tags", []):
            lines.append(f"@{tag}")
        lines.append(f"  Scenario: {scenario['title']}")
        lines.extend(f"    {step}" for step in scenario.get("steps", []))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_xray(data: dict) -> str:
    lines: list[str] = []
    for tag in data.get("feature_tags", []):
        lines.append(f"@{tag}")
    lines.extend(
        [
            f"Feature: {data['feature_title']}",
            f"  As a {data['persona']}",
            f"  I want {data['behavior']}",
            f"  So that {data['value']}",
            "",
        ]
    )
    for scenario in data.get("scenarios", []):
        lines.append(f"  Scenario: {scenario['title']}")
        lines.extend(f"    {step}" for step in scenario.get("steps", []))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_zephyr(data: dict) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(
        [
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
    )
    for test_case in data.get("zephyr_test_cases", []):
        steps = test_case.get("steps", [])
        for index, step in enumerate(steps):
            if index == 0:
                writer.writerow(
                    [
                        test_case.get("folder", "Imported Tests"),
                        test_case["name"],
                        test_case.get("objective", ""),
                        test_case.get("status", "Draft"),
                        test_case.get("precondition", ""),
                        " ".join(test_case.get("labels", [])),
                        step.get("step", ""),
                        step.get("expected_result", ""),
                        test_case.get("execution_type", "Manual"),
                        test_case.get("priority", "Medium"),
                        test_case.get("estimated_time", "5m"),
                        test_case.get("is_open", "Yes"),
                    ]
                )
            else:
                writer.writerow(["", "", "", "", "", "", step.get("step", ""), step.get("expected_result", ""), "", "", "", ""])
    return buffer.getvalue()


RENDERERS = {
    "markdown": render_markdown_detail,
    "tdd": render_markdown_detail,
    "summary": render_summary,
    "plain_text": render_plain_text,
    "bdd": render_bdd,
    "xray": render_xray,
    "zephyr": render_zephyr,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render a test artifact from normalized JSON.")
    parser.add_argument("format", choices=sorted(RENDERERS))
    parser.add_argument("source", help="Path to normalized JSON source")
    parser.add_argument("output", help="Path to write the rendered artifact")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    source_path = Path(args.source)
    output_path = Path(args.output)
    data = _read_json(source_path)
    text = RENDERERS[args.format](data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    print(f"Rendered {args.format} artifact to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
