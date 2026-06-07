# Clone And Run

This guide verifies the public CodeLanes repo from a clean clone.

## Clone

```bash
git clone https://github.com/agentwave-dev/CodeLanes.git
cd CodeLanes
```

## Run Validation

```bash
scripts/wave smoke
scripts/wave audit
scripts/wave context-pack --lane demo-lane --skill token-efficient-codex-run --goal "run fake-app tests"
python -m pytest examples/fake-app/tests
```

## Inspect The Harness

```bash
sed -n '1,180p' README.md
sed -n '1,220p' docs/articles/codelanes-technical-introduction.md
find docs/concepts -maxdepth 1 -type f | sort
```

## Try A Bounded Fake-App Run

```bash
WAVE_TASK_ID=demo-lane scripts/wave-run-detached demo-lane "python -m pytest examples/fake-app/tests"
scripts/wave peek --task demo-lane
scripts/wave-status
```

The detached run writes runtime output under `.agent-wave/runtime` and marker files under `/tmp`. Treat raw logs as local coordination state. `scripts/wave peek` reports active process, done marker, log size, completion JSON readiness, and narrow status lines without catting the log.
