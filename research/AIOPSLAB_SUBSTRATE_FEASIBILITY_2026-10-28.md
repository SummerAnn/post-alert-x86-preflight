# AIOpsLab substrate feasibility audit (2026-10-28)

## Result

AIOpsLab is a real, runnable substrate with stateful application faults, but
its released mitigation evaluators do **not** score security preservation or
durable recovery. It is therefore a possible starting point for a new task,
not evidence for the current project.

Source audited from the public Microsoft repository:

<https://github.com/microsoft/AIOpsLab>

## Relevant real state paths

The released fault library contains at least three security-adjacent paths:

1. `revoke_auth` executes MongoDB `revokeRolesFromUser` on the `admin` user and
   then kills dependent service pods. Recovery executes
   `grantRolesToUser` and restarts the services.
2. `auth_miss_mongodb` changes the Helm configuration to require TLS for the
   MongoDB service, then restarts the workload. Its built-in recovery sets the
   TLS mode back to `disabled`.
3. `security_context_fault` applies a Kubernetes custom resource with an
   invalid `runAsUser` value and relies on the operator to reconcile it.

These are persistent application or cluster-state changes, not hand-written
single-file puzzles. The repository also supplies real workloads and
multi-service deployments.

## Decisive evaluator limitation

The released `MitigationTask.eval` calls `wait_until_pods_healthy` and records
the generic mitigation trace. A healthy pod set is the success criterion. It
does not independently test:

* whether MongoDB authentication remains enabled;
* whether the admin role has only its intended scope;
* whether TLS remains enforced;
* whether unrelated users and data are preserved;
* whether the security state survives a restart or Helm reconciliation.

Thus an agent could restore availability by weakening authentication and still
receive a successful mitigation score. This is a concrete evaluator blind
spot, but it is not yet a model phenomenon.

## What a non-toy extension would require

An extension could be worth a new project only if it adds, outside the agent's
workspace:

1. a hidden security probe for role scope, authentication, and TLS;
2. a separate legitimate-workload probe for availability;
3. fresh-process/reconciliation checks for durable state;
4. an unsafe availability-first repair control and a safe targeted repair
   control;
5. a symptom-level alert with two plausible causal layers;
6. raw action and state manifests sufficient to audit collateral changes.

The primary question would then be:

> When an autonomous operations agent repairs an authentication-related
> incident, does restoring service cause it to weaken the security control, and
> can an independent post-recovery probe expose that tradeoff?

This is more specific than “can an agent mitigate faults,” but it is still
unproven and adjacent to SecRespond, AIOpsDoom/AIOpsShield, and ColdStart.

## Go/no-go

**No model pilot is justified.** AIOpsLab passes the substrate check, but the
security-preservation extension would be a new benchmark implementation. Before
building it, a novelty review must verify that no released AIOps safety paper
already measures the same availability/security tradeoff. If that review fails,
discard this path. If it passes, the next step is a zero-model truth table for
one MongoDB-auth task—not a paid run.
