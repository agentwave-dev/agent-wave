# bounded-healing

Use this skill after a failed run when repair is allowed and the attempt budget is explicit.

Steps:

1. Confirm the failed receipt or failed validation command.
2. Confirm the maximum attempt count.
3. Classify one failure type.
4. Make the smallest scoped repair.
5. Run the relevant validation command.
6. Write `templates/healing-receipt.md`.
7. Link the healing receipt into the Trace Graph.
8. Stop when validation passes, the failure class changes, or the attempt budget is exhausted.
9. Leave merge posture as `pending-human-review`.
