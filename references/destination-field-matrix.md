# Destination Field Matrix

Use this matrix before rendering. Ask only for missing fields that are required for the chosen destination.

## Legend

- `Required`: do not render the final artifact without it
- `Preferred`: render when present, but do not block
- `Optional`: include only when already known

## Detailed Markdown / TDD

| Field | Requirement | Notes |
|---|---|---|
| title | Required | Primary scenario name |
| steps | Required | Ordered actions and expected results |
| preconditions | Preferred | Include meaningful setup only |
| traceability | Preferred | Preserve stable IDs |
| execution_type | Optional | Defaults may be shown in the template |
| design_status | Optional | Defaults may be shown in the template |

## Summary Markdown

| Field | Requirement | Notes |
|---|---|---|
| id | Preferred | Keep stable when available |
| title | Required | Short readable row label |
| objective | Preferred | Useful for reviewers |
| coverage | Optional | Use only if already known |
| notes | Optional | Keep concise |

## Plain Text

| Field | Requirement | Notes |
|---|---|---|
| id | Preferred | Useful for traceability |
| title | Required | Keep readable |
| preconditions | Preferred | Can be short |
| expected_outcome | Required | Final observable result |

## BDD / Gherkin

| Field | Requirement | Notes |
|---|---|---|
| feature_title | Required | One feature per logical behavior group |
| scenarios | Required | At least one scenario |
| scenarios[].title | Required | Scenario name |
| scenarios[].steps | Required | Given/When/Then flow |
| feature_tags | Optional | Use only when meaningful |
| scenarios[].tags | Optional | Use only when meaningful |
| background | Optional | Use when shared setup improves clarity |

## Xray `.feature` / Bundle

| Field | Requirement | Notes |
|---|---|---|
| feature_title | Required | Valid Gherkin feature title |
| scenarios | Required | One or more valid Gherkin scenarios |
| scenarios[].title | Required | Required by feature syntax |
| scenarios[].steps | Required | Must stay valid Gherkin |
| tags | Preferred | Requirement tags improve traceability |
| zip packaging flag | Optional | Needed only for bundle workflows |

## Zephyr Scale CSV

| Field | Requirement | Notes |
|---|---|---|
| folder | Required | Default only if the workflow explicitly allows it |
| name | Required | Test case name |
| objective | Required | Short objective statement |
| status | Required | Example: Draft |
| precondition | Required | Empty only if the contract allows it |
| steps | Required | At least one step row |
| execution_type | Required | Example: Manual |
| priority | Required | Example: Medium |
| estimated_time | Required | Example: 5m |
| is_open | Required | Example: Yes |
| labels | Optional | Space-separated in the bundled template |

## TestLink-Oriented Mapping

| Field | Requirement | Notes |
|---|---|---|
| title | Required | Core case title |
| summary | Preferred | Derive only from provided content |
| preconditions | Preferred | Preserve when available |
| steps | Required | Ordered steps if the import path needs them |
| expected_results | Required | Keep paired with steps when possible |
| suite_or_section | Preferred | Ask when the workflow depends on hierarchy |

## TestRail-Oriented Mapping

| Field | Requirement | Notes |
|---|---|---|
| title | Required | Canonical case title |
| preconditions | Preferred | Include when known |
| steps | Required | Ordered steps |
| expected_results | Required | Preserve expected behavior |
| section | Preferred | Ask when hierarchy matters |
| custom_fields | Optional | Include only when explicitly provided |
