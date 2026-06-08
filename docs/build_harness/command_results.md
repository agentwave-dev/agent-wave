# CommandResult

`CommandResult` is a small structured observation contract for builder commands. It summarizes what happened without forcing the next loop to parse raw terminal output.

Fields:

- `success`: boolean result.
- `status`: `success`, `error`, or `blocked`.
- `summary`: compact human-readable observation.
- `artifacts`: paths created or updated.
- `next_actions`: recommended follow-up commands or operator actions.
- `recovery_hint`: optional guidance for errors or blockers.
- `raw_output_path`: optional path to bounded raw output when a command intentionally stores it.

Command output should be an observation, not a raw log dump. Future worker and repair loops should consume `CommandResult` objects and inspect referenced artifacts instead of scraping terminal text.
