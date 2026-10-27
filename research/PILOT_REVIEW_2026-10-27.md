# Pilot review and next gate

The first model pilot passed the immediate cleanup gate for both targeted and
capability-guided repair. Both preserved the legitimate incident command and
removed the hidden webhook API-key leak under an external probe.

The artifact is still insufficient for a dormant-residue claim. Although earlier
PRs introduce telemetry and environment-context pieces, the `--send` capability
and the verified exfiltration path appear only in the final PR. Rolling back one
PR therefore removes the feature entirely; there is no post-final archived PR in
this run on which to test a later-task trigger.

## Decision

Do not launch a confirmatory recovery comparison from this artifact alone. The
pilot validates the runner, not the intended scientific contrast.

The next gate is to acquire a second archived run with either (a) a side task
whose trigger is present before the final PR, or (b) an attack family with an
explicit fresh-process/later-PR postcondition. If no such artifact can be found,
the study should be reframed as immediate post-alert cleanup feasibility rather
than a dormant-persistence paper.
