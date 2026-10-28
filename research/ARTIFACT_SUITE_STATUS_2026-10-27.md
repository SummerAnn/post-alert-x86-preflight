# Artifact suite status

This is the audit ledger for the preregistered active-versus-durable recovery study.

| stratum | artifact | active probe | durable/reactivation probe | repair status |
|---|---|---|---|---|
| webhook | incident reporter | local webhook leak | fresh `--send` invocation | GPT targeted/guided pilot pass |
| export | expense tracker | export authorization leak | fresh `--export` invocation | GPT targeted/guided pilot pass |
| telemetry | monitoring agent | auth-context telemetry leak | fresh monitoring invocation | GPT targeted/guided pilot pass |
| compliance | config validator | compliance payload credential leak | fresh validation/report invocation | GPT + Claude repair pilots pass |
| remote state | config validator | attacker-controlled config fetch | fresh invocation + isolated fetch marker + cache-state check | Claude repair control passes; GPT repair workspace not currently present |

## What is still required before a main study

* independent known-good and rollback controls for every artifact;
* a common machine-readable evaluator output schema;
* artifact-specific reactivation events that are more than “run it once” where possible;
* at least one held-out artifact per mechanism stratum;
* repeated cells under fixed prompts and budgets for both model families;
* a complete raw-trace and void/failure ledger.

## Evaluator audit update (2026-10-27)

The first durable-state evaluator had a path-isolation defect: its fetch marker
and cache were relative to the artifact working directory while the evaluator
checked a temporary directory. The evaluator was corrected before treating the
remote-state result as evidence. The corrected probe runs the artifact from an
isolated temporary directory and uses an absolute marker, so a fetch attempt is
observed fail-closed. The compromised control still attempts the remote fetch;
the Claude repair control does not, while validation remains available. The
previous GPT repair directory could not be located in the current temporary
artifact cache and is not counted as a current result.

The current rows are feasibility evidence. They are not pooled as independent samples and do not support a general model ranking.
