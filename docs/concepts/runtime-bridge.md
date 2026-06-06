# Runtime Bridge

The runtime bridge is a narrow, sanitized channel from detached execution into repo-visible evidence.

Recommended bridge files:

- `normalized_event.json`: one small event with run id, lane, status, command, and timestamps.
- `reports/<run>.md`: human-readable run summary.
- `receipts/<run>.md`: completion receipt with tests and blockers.

Raw logs can stay outside the repository. If logs are committed as fixtures, use fake content only.

