# Amendment: SREGym-only exploratory feedback pilot — 2026-10-30

**Status:** frozen before any model calls. Exploratory only; not a replacement for
the blocked two-system confirmatory study.

## Reason for the bounded amendment

The frozen verifier-feedback design requires a native-compatible AIOpsLab
runtime. The available local Kubernetes node is ARM64, while the released
AIOpsLab deployment path is documented and tested for amd64/x86. Running an
ARM-rebuilt image would confound the cross-system study, so the AIOpsLab arm is
not launched here.

SREGym's released PSA task has passed the live mechanical truth table through
the checkpoint controller. A small SREGym-only pilot is allowed to test whether
the proposed feedback intervention produces any agent behavior worth pursuing;
it cannot support a cross-system or broad model claim.

## Frozen exploratory matrix

* system: SREGym `PSARestrictedBlocksRecreation` at the pinned release commit;
* models: `gpt-6.1-sol` and `claude-sonnet-4-6` (resolved identifiers recorded);
* conditions: health-only feedback and security-aware feedback;
* one fresh disposable episode per model × condition (four episodes total);
* maximum eight model turns and two nonterminal checkpoints per episode;
* identical initial alert, tools, namespace, state, and budgets within each
  model; only the checkpoint payload differs;
* hidden security probes remain outside the agent-visible process and payload;
* the released readiness oracle is called at checkpoints and at finalization;
* every episode is torn down even on error; no result is imputed.

## Interpretation

This pilot is a feasibility/behavior observation. It may justify a new
preregistration only if the intervention is delivered without leakage and the
two conditions produce a directional policy difference. A null, invalid, or
incomplete pilot closes this branch without scaling. No result from these four
episodes is a main-track claim.

