# Formatting Guidelines

Use this file when rendering output, not when choosing the test logic.

## General Rules

- Preserve stable IDs when they already exist.
- Preserve traceability without bloating the artifact.
- Use the smallest artifact that satisfies the destination.
- Keep source facts separate from inferred layout decisions.

## Detailed Markdown / TDD

- Start with the scenario title, not with generic prose.
- Prefer explicit preconditions and a step table over long narrative paragraphs.
- Keep metadata compact and auditable.

## Summary Markdown

- Favor scanability over completeness.
- Keep the same columns across comparable exports.
- Avoid multi-line cell content unless the user explicitly wants dense detail.

## Plain Text

- Keep each line actionable and reviewable.
- Prefer one scenario per row or bullet.
- Do not turn plain-text output into a pseudo-template with noisy labels.

## BDD Feature Output

- Use plain Gherkin with `Feature`, `Scenario`, `Given`, `When`, and `Then`.
- Keep each scenario focused on one observable behavior.
- Add tags only when they add meaningful traceability or execution value.

## Xray Gherkin Output

- Keep feature files valid plain Gherkin.
- Preserve stable tags when traceability exists.
- Keep the artifact portable so it can be imported directly or packaged into a zip bundle.

## Zephyr Scale CSV

- Do not generate a CSV row until every required field is known.
- Escape embedded quotes, commas, or newlines before rendering.
- Repeat parent test case metadata only where the import contract requires it.

## TestLink / TestRail Mappings

- Preserve the source meaning even if the destination hierarchy is incomplete.
- Return a mapping plan first when the final import path is unclear.
- Use placeholders only when the target workflow explicitly permits them.

## Formatting Guardrails

- Do not invent metadata just to satisfy a template.
- Do not mix analysis commentary into import-ready output.
- If the user wants a human-review artifact, optimize for clarity instead of raw import syntax.
