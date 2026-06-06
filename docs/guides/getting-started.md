# Getting Started

1. Clone or create a local Agent Wave repo.
2. Copy `templates/state-pack.yaml` into `.agent-wave/lanes/demo.yaml`.
3. Create `.agent-wave/state/demo.json` using the state pack fields from the docs.
4. Run `scripts/wave smoke`.
5. Run `scripts/wave audit`.
6. Start a detached run with `scripts/wave-run-detached demo "python -m pytest examples/fake-app/tests"`.
7. Write a receipt from `templates/completion-receipt.md`.
8. Run `scripts/wave milestone`.

