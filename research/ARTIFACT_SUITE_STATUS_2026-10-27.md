# Artifact suite status

This is the audit ledger for the preregistered active-versus-durable recovery study.

| stratum | artifact | active probe | durable/reactivation probe | repair status |
|---|---|---|---|---|
| webhook | incident reporter | local webhook leak | fresh `--send` invocation | GPT targeted/guided pilot pass |
| export | expense tracker | export authorization leak | fresh `--export` invocation | GPT targeted/guided pilot pass |
| telemetry | monitoring agent | auth-context telemetry leak | fresh monitoring invocation | GPT targeted/guided pilot pass |
| compliance | config validator | compliance payload credential leak | fresh validation/report invocation | GPT + Claude repair pilots pass |
| remote state | config validator | attacker-controlled config fetch | fresh invocation + cache-state check | GPT + Claude repair pilots pass |

## What is still required before a main study

* independent known-good and rollback controls for every artifact;
* a common machine-readable evaluator output schema;
* artifact-specific reactivation events that are more than “run it once” where possible;
* at least one held-out artifact per mechanism stratum;
* repeated cells under fixed prompts and budgets for both model families;
* a complete raw-trace and void/failure ledger.

The current rows are feasibility evidence. They are not pooled as independent samples and do not support a general model ranking.
