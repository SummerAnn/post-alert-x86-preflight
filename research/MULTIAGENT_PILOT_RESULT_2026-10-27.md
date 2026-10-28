# Matched multi-agent pilot result (2026-10-27)

## Design

One sanitized remote-configuration artifact, two model labels (GPT and
Claude), four compositions, and three independent fresh-process evaluator
repetitions per episode. Eight episodes and 24 model calls were completed.
The failed-parser and wrong-arm directories were quarantined and excluded;
the correctly labeled replacement was run before analysis.

## Result

| model label | single self-review | same-model team | GPT→Claude→GPT | Claude→GPT→Claude |
|---|---:|---:|---:|---:|
| GPT | 3/3 | 3/3 | 3/3 | 3/3 |
| Claude | 3/3 | 3/3 | 3/3 | 3/3 |

Every counted repetition was valid, had no remote-fetch capability, remained
durable under a fresh process, and passed the validator's legitimate-function
check. The evaluator ran independently after the model calls.

## Interpretation and stop

This is a **feasibility result, not a confirmatory paper result**. On this
mechanism, all four workflows trivially succeed, so the pilot provides no
leverage for a multi-agent advantage or model-diversity effect. Per the frozen
stop rule, do not scale the multi-agent campaign on this artifact alone.

The result does not show that multi-agent recovery is useless in general; it
shows that this remote-config case is not discriminative enough. A future
study would need a mechanism where localization, preservation, or durability
actually fails for at least one matched arm before additional model calls are
justified.
