---
name: test-artifact-export-skill
description: Format already-designed test cases, scenarios, or approved test artifacts into review-ready markdown, TDD-style case specs, plain-text scenario notes, BDD/Gherkin feature files, Xray-compatible Gherkin bundles, Zephyr Scale CSV, TestLink-oriented mappings, or TestRail-oriented mappings. Use when the test logic already exists and Codex must normalize, validate, and render it into a human-review or tool-import contract without inventing missing requirements or coverage.
metadata:
  author: jovd83
  version: "1.0.0"
---

# Test Artifact Export Skill

Render existing test-case content into a requested destination format. This skill is for formatting and export, not for test design, coverage generation, or requirements analysis.

## Scope

Use this skill only when the underlying test logic is already known through one of these inputs:

- approved test cases
- existing TDD, BDD, or plain-text test descriptions
- manually curated scenario lists
- framework-specific narrative test documentation
- normalized scenario data prepared by another skill or workflow

Do not use this skill to:

- choose a black-box test technique
- generate new coverage from requirements
- invent missing business rules, steps, or expected outcomes
- reverse-engineer unsupported vendor schemas from the web

If the user needs test design first, route them to the relevant test-design or test-planning skill before formatting.

## Read In This Order

1. `./references/formatter-guide.md`
2. `./references/normalized-test-case-model.md`
3. `./references/destination-field-matrix.md`
4. `./references/formatting-guidelines.md`
5. Read the destination-specific template or reference only for the chosen output:
   - `./assets/templates/test-case.j2`
   - `./assets/templates/tdd-summary-table.j2`
   - `./assets/templates/plain-text-list.j2`
   - `./assets/templates/bdd-feature.j2`
   - `./assets/templates/xray-gherkin.feature.j2`
   - `./assets/templates/zephyr-scale.csv.j2`
   - `./references/xray-gherkin-import.md`
   - `./references/testlink-import-file-formats.pdf`

## Supported Destinations

### Human-review outputs

- detailed markdown test case
- TDD-style markdown test case
- markdown summary table
- plain-text scenario notes
- BDD/Gherkin feature text

### Tool-oriented outputs

- Xray-compatible `.feature` files
- Xray-compatible zipped feature bundles when the workflow explicitly needs a zip
- Zephyr Scale CSV
- TestLink-oriented mapping output based on the bundled reference
- TestRail-oriented mapping output when the target fields are known

## Runtime Inputs

Capture these signals when present:

- target destination
- source artifact type
- scenario grouping such as feature, suite, folder, section, or component
- traceability IDs such as story, requirement, ticket, or test IDs
- metadata such as priority, labels, status, execution type, or owner
- whether the user wants artifact-only output or a mapping preview first
- whether the user needs one file, many files, or a zipped bundle

If the destination is ambiguous but low-risk, infer the most likely format and state the assumption. If the destination changes required fields or the output contract materially, pause for one focused clarification.

## Normalized Working Model

Normalize the source artifact into the minimal stable structure described in `./references/normalized-test-case-model.md`.

At minimum, try to extract:

- scenario identifier
- title
- objective or behavior
- preconditions
- ordered steps or Given/When/Then flow
- expected result or observable outcome
- traceability references
- destination-specific metadata if already known

Do not persist this runtime normalization automatically.

## Memory Model

- Runtime memory: use a temporary normalized case model and missing-field checklist for the current task only.
- Project-local persistent memory: create files only when the user asked for durable artifacts such as exported feature files, CSVs, or markdown case documents in their repo.
- Shared memory: out of scope. If cross-project reuse is needed, integrate an external shared-memory skill instead of storing reusable knowledge in this skill implicitly.

Do not automatically promote runtime notes into project-local or shared memory.

## Execution Workflow

### 1. Classify the Request

- Confirm that the user already has test logic.
- Identify the destination format.
- Determine whether the output is human-review, import-ready, or a mapping preview.

### 2. Normalize the Source

- Convert the source into the normalized working model.
- Preserve only fields that are actually present.
- Keep source facts separate from inferred structure.

### 3. Check Destination Requirements

- Use `./references/destination-field-matrix.md`.
- Build a short missing-field list only for fields that are required by the chosen destination.
- Ask for missing required fields instead of inventing them.

### 4. Render the Artifact

- Use the destination-specific template or reference contract.
- Preserve traceability when it exists.
- Keep import-ready outputs free of analysis commentary.

### 5. Validate When Possible

- Use `python ./scripts/format-validator.py markdown <path>` for detailed markdown or TDD-style markdown that uses the bundled structure.
- Use `python ./scripts/format-validator.py summary <path>` for summary-table markdown.
- Use `python ./scripts/format-validator.py plain_text <path>` for lightweight plain-text artifacts.
- Use `python ./scripts/format-validator.py bdd <path>` for generic Gherkin.
- Use `python ./scripts/format-validator.py xray <path>` for Xray `.feature` files or zipped feature bundles.
- Use `python ./scripts/format-validator.py zephyr <path>` for Zephyr Scale CSV.

If a destination has no deterministic validator in this repo, say that clearly and validate the source-to-destination field mapping manually instead of pretending stronger verification than exists.

### 6. Return the Right Final Shape

- For import-ready destinations, return only the artifact unless a missing-field or ambiguity block remains.
- For mapping previews, return the field mapping plus unresolved gaps.
- For human-review outputs, optimize for readability and stable identifiers.

## Destination Rules

### Detailed Markdown Or TDD

- Use `test-case.j2`.
- Keep one scenario per canonical case artifact unless the user explicitly asks for a summary-only deliverable.
- Use the step table with `Step | Action | Expected Result`.

### Summary Markdown

- Use `tdd-summary-table.j2`.
- Keep the summary compact and stable across revisions.

### Plain Text

- Use `plain-text-list.j2` only for lightweight review output.
- Keep each row readable and decision-oriented rather than verbose prose.

### BDD / Gherkin

- Use `bdd-feature.j2`.
- Keep each scenario focused on one observable behavior.
- Add tags only when they add real traceability or execution meaning.

### Xray

- Stay inside `.feature` file import support described in `./references/xray-gherkin-import.md`.
- Use `xray-gherkin.feature.j2`.
- Package zipped bundles only when the surrounding workflow explicitly requires a zip.
- Do not invent unsupported Xray JSON schemas.

### Zephyr Scale

- Use `zephyr-scale.csv.j2`.
- Do not render the CSV until all required columns are known.
- Repeat parent case metadata only as required by the CSV contract.

### TestLink / TestRail

- Prefer a mapping-first workflow when the import shape is ambiguous.
- Stay within fields supported by the source artifact and bundled references.
- If the user requests a concrete import payload but the destination contract is incomplete or ambiguous in this repo, say so plainly and return the mapping plan instead of fabricating a schema.

## Failure And Escalation Rules

- If the source artifact is incomplete for the requested destination, ask only for the missing required fields.
- If the source mixes designed and undesigned scenarios, format only the designed subset and call out the blocked items.
- If the user requests an unsupported tool or schema, say it is unsupported in the current implementation.
- If multiple output destinations are requested, complete them one at a time from the same normalized model.

## Researching New Destinations

If the user asks for a new output format that this repository does not yet support:

1. Confirm that the task is to extend the skill, not merely to describe the format.
2. Research the destination using primary or official sources only.
3. Capture the contract locally before claiming support:
   - add or update a reference under `./references/`
   - extend `./references/destination-field-matrix.md`
   - add templates or static assets under `./assets/templates/` when rendering is deterministic
   - add or extend validator logic only when local deterministic checks are feasible
   - add source and expected examples under `./examples/`
   - add or extend automated tests under `./tests/`
4. State what was verified, what remains ambiguous, and whether the new destination is artifact-ready or mapping-only.

Use `./references/new-destination-research-workflow.md` and `./scripts/scaffold-new-destination.py` to keep this expansion path structured and auditable.

## Guardrails

- Do not redesign coverage.
- Do not add missing business logic.
- Do not silently assign invented metadata.
- Do not mix analysis commentary into import-ready artifacts.
- Do not claim a destination is validated when the repo only supports heuristic checks.
- Do not turn runtime normalization into persistent skill memory.
- Do not claim support for a newly researched destination until the repo contains the necessary references, examples, and tests.

## Extensibility Hooks

- Add new destinations by extending `./references/destination-field-matrix.md`, adding or updating the relevant template or reference contract, and teaching `./scripts/format-validator.py` only when deterministic validation is feasible.
- Keep destination-specific behavior in references and templates, not bloated into this file.
- Preserve backward compatibility for existing destination names unless there is a clear migration reason.
