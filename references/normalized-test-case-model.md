# Normalized Test Case Model

Use this model as the runtime-only working structure before rendering any destination.

Do not require every field for every destination. Normalize only what is present and check the chosen destination for required fields afterward.

## Core Scenario Fields

- `id`: stable scenario identifier when available
- `title`: concise scenario title
- `objective`: short statement of the behavior or verification goal
- `description`: optional narrative context
- `preconditions`: ordered list of required starting conditions
- `steps[]`: ordered list of execution steps
- `steps[].action`: user, system, or API action
- `steps[].expected_result`: expected observable result for that step
- `expected_outcome`: optional final outcome summary for lighter-weight outputs
- `traceability[]`: requirement, story, ticket, or contract references

## Grouping Fields

- `feature_title`
- `suite`
- `folder`
- `section`
- `component`

## Metadata Fields

- `status`
- `priority`
- `labels[]`
- `execution_type`
- `estimated_time`
- `owner`
- `test_level`
- `notes`

## BDD-Oriented Fields

- `feature_tags[]`
- `background[]`
- `persona`
- `behavior`
- `value`
- `scenarios[]`
- `scenarios[].title`
- `scenarios[].tags[]`
- `scenarios[].steps[]`

## Destination-Specific Notes

- Markdown and TDD usually consume `title`, `preconditions`, `steps`, and metadata.
- Plain-text output can rely on `id`, `title`, `preconditions`, and `expected_outcome`.
- Zephyr Scale expects flat per-step rows after normalization.
- Xray feature output expects valid Gherkin-ready scenario structures.
- TestLink and TestRail paths should prefer field mappings when the final import structure is not fully known.
