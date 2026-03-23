# New Destination Research Workflow

Use this workflow when a user asks the skill to support a destination that is not yet implemented in this repository.

## Goal

Add a new output destination in a way that is auditable, minimally risky, and easy to maintain.

## Research Rules

- Use primary or official sources only.
- Prefer vendor documentation, official product docs, or first-party import examples.
- Record uncertainty explicitly instead of smoothing over it.

## Required Deliverables

1. A checked-in reference note that summarizes the supported contract and source links.
2. An update to `destination-field-matrix.md`.
3. A rendering path:
   - template-backed artifact generation, or
   - mapping-only output when full rendering is still ambiguous.
4. At least one source example and one expected output or mapping example.
5. Automated tests for the new path.

## Decision Criteria

Choose `artifact-ready` only when:

- the destination contract is well-defined,
- the required fields are known,
- the repository can render the final output deterministically.

Choose `mapping-only` when:

- the repository can map fields reliably,
- but cannot yet guarantee a valid final import payload.

## Do Not

- claim support based on secondary summaries,
- claim a vendor API integration when the repo only supports offline export,
- add validator logic that merely echoes the template shape without meaningful contract checks.
