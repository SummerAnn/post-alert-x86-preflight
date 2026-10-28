# AIOpsLab zero-model adapter gate

**Date:** 2026-10-28  
**Status:** blocked before live execution  
**Model/API calls:** 0  
**External mutations:** 0

## Purpose

This was the first feasibility step for the AIOpsLab route. It audits the
released source and checks whether a live Kubernetes context is available. It
does not inject a fault, modify a deployment, invoke an agent, or change the
official evaluator.

## Source gate: PASS

The checked-out public source at
`/private/tmp/aiopslab-audit.t50o83/src` contains all required ingredients:

* MongoDB `revokeRolesFromUser` fault scripts;
* matching `grantRolesToUser` recovery scripts;
* the `auth_miss_mongodb` TLS fault (`requireTLS`);
* the corresponding TLS rollback (`disabled`);
* official mitigation classes whose success assignment is based on
  `wait_until_pods_healthy`;
* no role, authentication, TLS, or preservation probe in those success
  assignments.

The deterministic source check is implemented in
`feasibility/aiopslab_zero_model_gate.py`.

## Live gate: BLOCKED

The local machine has `kubectl`, but no current Kubernetes context:

```text
error: current-context is not set
```

Consequently there is no safe way to run the truth table here. Starting a
cluster or pulling AIOpsLab images would be infrastructure work and would not
by itself establish a scientific result. No workaround or synthetic local
cluster is being substituted.

## Required live truth table if a cluster becomes available

The adapter must run the official AIOpsLab evaluator unchanged and compare its
result with an external oracle for each state:

| state | service/workload | auth/TLS security | restart/reconciliation | expected official gate |
|---|---|---|---|---|
| clean | healthy | restored | passes | success |
| safe repair | healthy | restored | passes | success |
| availability-first repair | healthy | weakened | passes | potentially false success |
| rollback/control | unavailable or disabled | capability removed | passes | failure or collateral damage |

The hidden oracle must query the actual MongoDB role/TLS behavior, an unrelated
legitimate workload, and the post-restart state. It must not expose its
expected values to an agent. A single static source match is not evidence of a
blind spot.

## Decision

The AIOpsLab path is **technically feasible in source** but **not runnable in
this environment yet**. It remains a candidate adapter, not a paper result.
No model pilot is authorized by this gate. The next requirement is a real,
isolated Kubernetes environment and a second independent system before any
main-track claim is considered.

