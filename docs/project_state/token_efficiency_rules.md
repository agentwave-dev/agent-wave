# Token Efficiency Rules

Use these rules in generated prompts, lane files, skills, and completion receipts.

## Required

- Read the state pack first.
- Do not restate project history.
- Read only target files listed in the prompt.
- Do not scan unrelated files.
- Do not print full diffs.
- Do not print full files.
- Write a heartbeat artifact before deep work.
- Write compact completion JSON.
- If log output exceeds the configured cap, stop broad exploration and summarize.
- Prefer artifact paths over inline logs.
- Use summary extraction commands instead of `cat` or broad `tail`.

## Forbidden

- No raw logs in chat, docs, receipts, or context packs.
- No full project canvas pasted into a run prompt.
- No full completion markdown pasted back into ChatGPT.
- No secrets, tokens, private tenant data, customer data, or `.env` content.

## Default Budgets

- Context pack: 200 lines.
- Completion receipt: 120 lines.
- Log inspection: size, readiness, done marker, active process, and narrow status grep only.
