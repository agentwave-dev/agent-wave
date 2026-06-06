# Codex CLI Guide

Use Codex CLI as a detached runner by wrapping it with `scripts/wave-run-detached`.

Example:

```bash
scripts/wave-run-detached demo-lane "codex exec --full-auto - < templates/lane.prompt.md"
```

The wrapper records a run directory, command, exit code, and receipt pointer. Keep prompts generic and avoid private runtime data.

