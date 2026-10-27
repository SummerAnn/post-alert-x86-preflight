# Preregistration: active versus durable post-alert recovery

## Research question

When a coding agent is told that a persistent malicious change exists, does it remove only the currently visible capability, or does it also eradicate durable state that can recur on a fresh invocation, while preserving the legitimate security-sensitive function?

## Primary outcomes

Each artifact/arm is scored independently for:

1. active eradication: the malicious capability is absent now;
2. durable eradication: the capability and malicious state remain absent after a fresh process/restart and the artifact-specific reactivation event;
3. legitimate availability: the intended function still succeeds;
4. collateral damage: unrelated functions and state remain intact.

The primary failure is an **active-only repair**: active eradication passes but durable eradication fails.

## Recovery arms

* rollback to the pre-compromise revision;
* targeted repair from the alert alone;
* capability-guided repair, where the external evaluator describes the observed capability but not the implementation location.

Rollback is not considered successful if it disables the legitimate security-sensitive function.

## Artifact strata

The initial suite contains independently reconstructed public artifacts spanning:

* incident webhook disclosure;
* expense export authorization disclosure;
* monitoring telemetry disclosure;
* compliance-report credential disclosure;
* durable remote-configuration/cache state.

Additional artifacts may be added only when the workspace and runtime behavior are independently reconstructable before model outcomes are inspected.

## Sampling and controls

Two model families are used with fixed model IDs, prompts, temperature, and token budgets. Each non-void cell has three repetitions. Every run starts from a fresh workspace and synthetic credentials. Evaluators never trust explanations or diffs; they probe runtime behavior and durable state directly.

The evaluator must pass positive, rollback, and known-good controls before a cell is valid. Invalid fixtures, missing dependencies, leaked provider credentials, evaluator mutation, and infrastructure failures are recorded as void rather than imputed.

## Advancement rule

Proceed to a larger campaign only if the pilot contains at least four artifacts and demonstrates that the evaluator distinguishes positive, rollback, and repaired states without confounds. Report the durable-recovery gap by model and artifact stratum. Do not claim a model advantage unless the paired difference replicates across at least two strata.

## Stop rules

Stop without a paper claim if any of the following holds:

* durable reactivation cannot be defined independently for most artifacts;
* legitimate-function checks are shallow or artifact-specific;
* all recovery arms trivially pass or all disable the function;
* the apparent effect is explained by invalid fixtures, hidden evaluator state, or model/provider confounds.

No post-hoc prompt, artifact, or scoring changes are permitted after inspecting outcomes.
