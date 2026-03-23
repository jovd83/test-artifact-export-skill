# Xray Gherkin Import Reference

This repository supports Xray through Gherkin `.feature` files and optional zipped feature bundles.

## Supported Contract

- one or more `.feature` files
- valid plain Gherkin syntax with `Feature`, `Scenario`, `Given`, `When`, and `Then`
- optional tags for traceability
- optional `.zip` packaging when a surrounding workflow requires a bundle

## Operating Rules

- Keep every exported file valid Gherkin first.
- Preserve requirement or story tags when they already exist.
- Use zip packaging only as a transport wrapper, not as a different content format.
- Validate each feature artifact before bundling.

## Out Of Scope

- unsupported Xray JSON payloads
- invented Jira linkage
- API publishing workflows
