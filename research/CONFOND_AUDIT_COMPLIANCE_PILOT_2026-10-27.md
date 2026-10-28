# Compliance pilot confound audit (2026-10-27)

Before any compliance model calls, the runner was found to include the
artifact's test files in the model prompt. Those files explicitly described
redaction expectations and could make the task a test-reading exercise.

The runner now hides the compliance tests and evaluator fixtures from every
role. The external evaluator still runs against the complete workspace, so the
model-visible and scorer-visible surfaces are separated. The same hidden-file
policy applies to all four arms and both model families.

The pilot remains blocked until the test-hidden visible-file set is checked for
the positive, rollback, and known-good controls. No compliance model calls were
made during this audit.
