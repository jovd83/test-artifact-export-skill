# Formatter Guide

Use this skill only after the test logic is already designed.

## Purpose

This repository exists to normalize approved test-case content and render it into review-ready or tool-ready output contracts.

The formatter is intentionally downstream of:

- requirements analysis
- test-case design
- coverage planning
- risk analysis

## Operating Principle

Treat every source artifact as incomplete until proven otherwise.

The correct behavior is:

1. normalize the source
2. determine the target destination
3. check which destination fields are truly required
4. ask for missing required fields
5. render only what the repo can support

## Decision Rules

- Prefer a direct artifact when the target contract is well-defined in this repository.
- Prefer a mapping-first response when the final vendor import shape is ambiguous.
- Prefer refusal over improvisation when the repository lacks a reliable contract.

## Supported Contract Strength

- Strong: markdown/TDD, summary markdown, plain text, BDD/Gherkin, Xray Gherkin, Zephyr CSV
- Moderate: TestLink-oriented mappings based on the bundled PDF
- Moderate: TestRail-oriented mappings when the required target fields are already known

## Unsupported Requests

If a user requests:

- a vendor schema not documented in this repo,
- direct publishing into a vendor API,
- auto-generated missing test logic,

say that it is out of scope for the current implementation instead of approximating it.
