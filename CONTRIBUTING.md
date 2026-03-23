# Contributing

Keep this repository narrow, deterministic, and easy to reason about.

## Contribution Principles

- Preserve the skill boundary: formatting and export only
- Prefer stronger contracts over broader but vague claims
- Add a new destination only when the repository can document its fields clearly
- Add validation only when deterministic local checks are possible
- Keep `SKILL.md` concise and move detailed destination guidance into `references/`

## When Adding A New Destination

1. Add or update the destination contract in `references/destination-field-matrix.md`.
2. Add or update the destination template or bundled reference.
3. Extend `SKILL.md` only as much as needed to expose the new capability.
4. Add at least one example input and expected output.
5. Add or update automated tests.
6. Update `README.md` if the public capability surface changed.
7. If the destination came from fresh research, cite the official or primary source in a checked-in reference note.

## Validation Checklist

Run:

```powershell
python C:\Users\jochi\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
python -m unittest discover -s tests -p "test_*.py"
```

If you changed the validator, add or update representative tests rather than relying on manual inspection only.

## Non-Goals

- Do not add speculative frameworks or placeholder files.
- Do not add shared-memory infrastructure here.
- Do not claim support for vendor formats that the repo cannot validate or document locally.
