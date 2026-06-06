# Forbidden Paths

Forbidden-path gates prevent accidental public release of private data and generated runtime state.

Use `templates/forbidden-paths.txt` as a baseline. Projects should add their own deny patterns for private configs, credentials, live runtime outputs, customer data, vendor exports, and machine-specific files.

The gate should run before detached runs, before receipt finalization, and before milestone commits.

