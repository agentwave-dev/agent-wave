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
scripts/wave-run-detached demo-lane "python -m pytest examples/fake-app/tests"
scripts/wave-status
```

The detached run writes runtime output under `.agent-wave/runtime`. Treat that as local coordination state. Do not commit raw logs or private runtime artifacts.
