# Amendment: matched multi-agent recovery comparison (2026-10-27)

## Purpose

Add a multi-agent condition without changing the artifact, evaluator, model,
or preservation objective. The comparison tests whether **restricted role
separation**, rather than simply more model calls, improves post-alert recovery.

## Question

Under an equal call and token budget, does a role-separated recovery team
remove persistent attacker capability more durably and preserve legitimate
function better than a single agent with the same number of self-review calls?

## Conditions

Each episode receives exactly three model calls from one pinned model family
and the same total output-token cap.

* **Single-agent self-review (control):** one agent identity receives the
  artifact and alert, then performs three sequential turns: diagnose, propose
  repair, and audit/revise. It sees its own prior transcript.
* **Role-separated team (primary treatment):** three calls use the same pinned model:
  a localizer, a repairer, and a reviewer. The localizer sees the artifact and
  alert and returns a structured finding; the repairer sees the artifact plus
  that finding but not the localizer's hidden chain-of-thought; the reviewer
  sees the artifact, proposed patch, and a fixed checklist but not hidden
  evaluator probes. The reviewer may return a bounded patch revision, but no
  fourth call is allowed.

Two exploratory heterogeneous teams use the same roles and total budget:

* **GPT→Claude→GPT:** GPT localizer, Claude repairer, GPT reviewer.
* **Claude→GPT→Claude:** Claude localizer, GPT repairer, Claude reviewer.

These arms are analyzed separately from the primary same-model comparison.
Both directions are required before making a model-diversity claim.

The model, temperature/reasoning setting, maximum output tokens, artifact,
randomized episode order, and total call cap are identical across conditions.
Prompts are frozen before any confirmatory calls.

## What is held constant

The same three mechanisms, positive controls, rollback controls, model
families, repair-replication count, evaluator, fresh-process repetitions, and
legitimate-function suites are used for both conditions. A single repair is not
replayed as independent evidence: each `(mechanism, model, arm, repair_rep)`
gets a fresh artifact and fresh model calls.

## Information-flow restrictions

The hidden capability probes, synthetic credentials, and evaluator outputs are
never shown to any model. The reviewer receives only the fixed preservation
checklist and observable source/runtime information. Handoffs are serialized
JSON with schema validation; malformed handoffs void the episode rather than
being repaired post hoc.

## Primary outcomes

For each independent repair artifact: capability active, durable capability
absence after fresh process/reactivation, legitimate function available, and
collateral damage. The primary comparison is durable recovery *with* preserved
legitimate function. Cost, call count, and latency are secondary outcomes.

## Required evidence before a claim

No role-separation advantage is claimed unless the primary treatment improves the
pre-registered primary outcome under the matched-budget comparison and the
effect is present in both model families. Otherwise the result is reported as
null or mechanism-specific. A successful reviewer patch alone is not evidence
of a team advantage unless the matched single-agent control receives the same
three-call opportunity. No model-diversity claim is made unless both
heterogeneous directions are complete and compared with their same-model arms.

## Stop rules

Stop before confirmatory calls if any handoff schema, budget accounting, or
blindness check fails; if the single-agent and team arms receive unequal
information or calls; if any control/evaluator differs by arm; or if the
artifact cannot distinguish a preserved feature from a disabled feature.
