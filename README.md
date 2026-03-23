# Test Artifact Export Skill

A standalone Agent Skill for turning already-designed test cases into clean review artifacts or tool-ready export artifacts.

This repository is intentionally focused on formatting and export. It does not generate new coverage, choose test-design techniques, or infer missing requirements. Its job is to take existing test logic, normalize it, check destination requirements, and render a reliable output contract.

## What This Skill Is Responsible For

- Formatting approved test cases into markdown, TDD-style markdown, plain text, or BDD/Gherkin
- Exporting approved test cases into Xray-compatible feature files, Zephyr Scale CSV, and mapping-oriented TestLink or TestRail outputs
- Preserving traceability and known metadata during conversion
- Refusing to invent missing business logic or destination metadata
- Providing deterministic validation where this repository has enough local contract knowledge

## What This Skill Is Not Responsible For

- Designing new test cases from requirements
- Choosing boundary-value, equivalence-partitioning, decision-table, or other test-design techniques
- Maintaining cross-agent shared memory
- Supporting every vendor schema on the internet

If you need test design first, run a test-design or planning skill before this one.

## Repository Structure

```text
.
|-- SKILL.md
|-- agents/openai.yaml
|-- assets/templates/
|-- examples/
|-- evals/
|-- references/
|-- scripts/
|-- schemas/
`-- tests/
```

## Supported Destinations

### Human-review artifacts

- Detailed markdown test cases
- TDD-style markdown
- Markdown summary tables
- Plain-text scenario notes
- BDD/Gherkin feature text

### Tool-oriented artifacts

- Xray `.feature` files
- Xray zipped feature bundles
- Zephyr Scale CSV
- TestLink-oriented field mappings
- TestRail-oriented field mappings

## Installation

Place this skill folder where your Codex-compatible skill runtime discovers skills. For local Codex setups that usually means:

- `%USERPROFILE%\\.codex\\skills\\test-artifact-export-skill`
- or another configured skills directory

The required entrypoint is [SKILL.md](./SKILL.md). UI metadata lives in [agents/openai.yaml](./agents/openai.yaml).

## How It Works

1. Read the source artifact and confirm the test logic already exists.
2. Normalize it into the repository's internal case model.
3. Check which required fields the target destination needs.
4. Ask only for missing required fields.
5. Render the artifact with the matching template or bundled contract.
6. Validate when a deterministic validator exists.

The repository also includes:

- `scripts/render-artifact.py` for deterministic rendering from a normalized JSON source
- `schemas/` for checked-in source and request contracts
- `scripts/scaffold-new-destination.py` for safely growing the repo when a new format is researched

## Validation And Testing

Validate the skill definition:

```powershell
python C:\Users\jochi\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
```

Run repository tests:

```powershell
python -m unittest discover -s tests -p "test_*.py"
python scripts/validate-repo.py
```

Render an artifact from the bundled example source:

```powershell
python scripts/render-artifact.py markdown examples\source\checkout-cases.json out\checkout-tdd.md
```

Run validator examples manually:

```powershell
python scripts/format-validator.py markdown examples\expected\checkout-tdd.md
python scripts/format-validator.py summary examples\expected\checkout-summary.md
python scripts/format-validator.py plain_text examples\expected\checkout-plain-text.md
python scripts/format-validator.py xray examples\expected\checkout-xray.feature
python scripts/format-validator.py zephyr examples\expected\checkout-zephyr.csv
```

## Examples

- Source artifact: [examples/source/checkout-cases.json](./examples/source/checkout-cases.json)
- Expected markdown: [examples/expected/checkout-tdd.md](./examples/expected/checkout-tdd.md)
- Expected summary: [examples/expected/checkout-summary.md](./examples/expected/checkout-summary.md)
- Expected plain text: [examples/expected/checkout-plain-text.md](./examples/expected/checkout-plain-text.md)
- Expected Xray feature: [examples/expected/checkout-xray.feature](./examples/expected/checkout-xray.feature)
- Expected Zephyr CSV: [examples/expected/checkout-zephyr.csv](./examples/expected/checkout-zephyr.csv)

## Memory Boundaries

- Runtime memory: transient normalized case model and missing-field checklist for one task
- Project-local persistent memory: exported artifacts written into the user's repository when requested
- Shared memory: external concern, not implemented in this skill

This separation is deliberate. Runtime formatting work should not silently become persistent memory.

## Optional Integrations

This skill fits well behind:

- test-design skills that generate approved scenarios
- framework-specific documentation skills that need a final formatter/exporter
- CI workflows that validate exported artifacts before import

These integrations are optional. The skill remains usable as a standalone formatter.

## Adding A New Destination Format

This repository supports a structured expansion workflow for new formats.

When a user asks for a format the repo does not yet support, the expected process is:

1. Research the destination from official or primary documentation.
2. Record the contract in `references/`.
3. Extend the destination field matrix.
4. Add templates or static assets only when deterministic rendering is realistic.
5. Add examples, tests, and validator logic where feasible.

Use:

```powershell
python scripts/scaffold-new-destination.py --name azure-devops --mode mapping
```

The scaffold is intentionally lightweight. It creates the repo slots that a contributor or agent should fill after research.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for repo expectations and change boundaries.

## Out Of Scope For This Repository

- Vendor APIs for publishing artifacts directly into test-management systems
- Full JSON schema support for every Xray/TestRail/TestLink import path
- Autonomous self-modification or implicit memory promotion
