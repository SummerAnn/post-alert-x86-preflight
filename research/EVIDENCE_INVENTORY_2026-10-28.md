# Repository-wide evidence inventory (2026-10-28)

## Executive decision

The repository does not currently contain a main-conference result. It contains
useful evaluator engineering, several reproducible feasibility observations,
one saturated multi-agent pilot, and multiple closed or invalidated branches.
No existing result supports a broad claim about recovery agents, multi-agent
advantage, or durable post-alert recovery.

Do not launch another model batch from this repository without first obtaining
an artifact that produces non-ceiling behavior under the already-built
evaluator.

## Evidence ledger

| item | what is actually supported | validity | strongest defensible use |
|---|---|---|---|
| Incident-reporter replay | A public archived final state can execute an API-key leak; rollback removes it; targeted and capability-guided repairs preserve the normal send path in the recorded feasibility checks. | Valid narrow feasibility evidence; not a powered study. | Demonstrates that the evaluator can separate eradication from preservation. |
| Expense-tracker durable enrichment | A remote enrichment path leaks a key and writes a cache across fresh processes. Rollback disables enrichment. A preservation-constrained GPT repair redirected the legitimate endpoint and retained the cache. | Valid narrow feasibility evidence; one artifact/model and reconstructed source. | Shows that durable state and preservation can be scored separately. |
| Monitoring/telemetry artifact | The pilot ledger reports a distinct telemetry-context leak with positive, rollback, targeted, and capability-guided states. | Feasibility evidence only; raw run data is not tracked here. | Possible third mechanism for a future study, not a result by itself. |
| Remote-config artifact | Corrected zero-model controls and fresh-process checks distinguish active fetch, rollback, and targeted repair. | Valid feasibility evidence, but one mechanism and archive-reconstructed. | A reusable durable-state evaluator case. |
| Matched multi-agent pilot | Four workflow compositions, two model labels, eight episodes, and three evaluator repetitions per episode all succeed (3/3). | Valid pilot result, but ceiling/single artifact. | Shows the chosen artifact cannot test multi-agent benefit. It is a stop, not a positive method result. |
| Compliance v2 audit | Exact archived artifact passes positive/targeted/rollback/decoy truth table under the exact command. | Valid audit result; candidate fails difficulty contract. | Justifies discarding the artifact before model calls. |
| Earlier compliance method-validation document | Reported successful GPT/Claude repairs using a different evaluator command and field names. | Superseded/void for the recovered artifact. | Must not be cited as evidence. |
| Confirmatory 54-cell study | A manifest exists, but no valid confirmatory result was produced. | Not run. | No scientific evidence. |
| Control-integrity hypothesis | Requires a monitor-visible surface that can diverge from effective behavior. | Design only; substrate absent. | Future idea, not evidence. |
| Evidence-preservation/state-reconstruction/handoff designs | Deterministic task sketches and literature comparisons exist. | Design only. | Candidate questions, not results. |

## What survives all audits

Three technical components are real and reusable:

1. external capability probes rather than trusting agent explanations or patch
   text;
2. separate scoring of capability removal, legitimate-function preservation,
   restart/reactivation, and collateral damage;
3. provenance and evaluator audits that can invalidate an attractive result
   before spending additional model calls.

These are infrastructure contributions. They are not yet a scientific finding
because the model responses are mostly universal successes on easy artifacts,
and the repo does not retain a complete raw-trace dataset for independent
reanalysis.

## Main confounds and evidence limits

### 1. Ceiling effects

The remote-config multi-agent pilot is 3/3 for every arm and model label. The
repair-arm pilots also report success across the retained cases. There is no
failure distribution from which to estimate an agent, model, or team effect.

### 2. One mechanism is not a benchmark

Repeated fresh-process probes are useful durability checks, but three
repetitions of one reconstructed workspace are not three independent attack
mechanisms. Most model evidence is one repair per artifact/model, not a sampled
set of incidents.

### 3. Same archive family and selection

The incident, expense, telemetry, and remote-config cases come from a small
set of public archive artifacts selected for reconstructability. Successful
reconstruction and completed repairs are overrepresented; this is feasibility
selection, not a representative benchmark sample.

### 4. Provenance is reconstruction, not original checkout

The source is rebuilt from archived diffs and trajectory views. That is enough
for a documented executable replay, but it is weaker than releasing the
original attacked workspace, dependencies, and raw model traces.

### 5. Evaluator drift and stale records

The compliance evaluator mismatch was discovered only after earlier pilot
records were written. The old command used unsupported flags and expected a
different report schema. The corrected audit invalidates those rows for the
recovered artifact. Similar stale status documents must not be pooled with the
latest gate result.

### 6. No independent held-out test set

All artifacts were used during design, reconstruction, or evaluator repair.
There is no held-out mechanism on which a preregistered recovery claim was
tested after the evaluator was frozen.

## Branches that should be closed or retained only as infrastructure

* **Compliance disclosure v2:** closed by the 2026-10-28 gate result.
* **Multi-agent advantage on remote-config:** stopped by the universal-success
  pilot.
* **Dormant-residue claim from the first incident replay:** unsupported because
  the executable trigger appears only in the final archived change.
* **Control-integrity gap:** unimplemented substrate; do not relabel existing
  recovery probes as this phenomenon.
* **Evidence-preservation and handoff questions:** promising design sketches,
  but no observed agent behavior and substantial overlap with existing work.
* **Earlier compliance method-validation and artifact-suite summaries:** retain
  for audit history, but mark superseded where they conflict with the corrected
  provenance result.

## What a real main-track result would still require

At minimum, a new artifact must satisfy all of the following before paid model
calls:

1. two independently implemented capability/persistence paths;
2. two plausible causal layers with one real causal repair and a realistic
   decoy;
3. a preservation function that rollback genuinely damages;
4. a fresh-process or declared durability event that can reactivate the attack;
5. an evaluator frozen before model outcomes are inspected;
6. repeated, raw, independently retained traces from more than one artifact;
7. non-ceiling behavior in a cheap one-model calibration.

If the candidate cannot meet these requirements without hand-invented state or
arbitrary obscurity, it should be discarded rather than made harder by adding
synthetic clutter.

## Recommendation

Freeze this repository as a rigorous feasibility and evaluator-audit record.
Do not spend more API credits on the current artifact suite. A main-track
attempt now requires a separately sourced, genuinely difficult application
incident, not another prompt, model, or repetition on these cases. If such an
artifact cannot be obtained, the honest output is an infrastructure/feasibility
write-up or closure of this research line.
