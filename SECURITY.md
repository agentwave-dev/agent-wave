# Security

CodeLanes is designed for local orchestration. Do not commit credentials, vendor tokens, private runtime artifacts, customer records, or machine-specific secrets.

## Reporting Issues

Open a private security advisory or contact the maintainers through the project security channel when one is available. For this local scaffold, file a local issue draft and avoid placing exploit details in public logs.

## Public Repo Rules

- Use fake examples only.
- Keep runtime outputs out of version control unless they are sanitized fixtures.
- Store lane expectations as paths and branch names, not credentials.
- Treat `.agent-wave/state` as durable coordination state, not a secret store.
- Run `scripts/wave audit` before milestone commits.
