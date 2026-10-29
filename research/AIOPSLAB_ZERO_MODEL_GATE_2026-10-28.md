# AIOpsLab zero-model adapter gate

**Date:** 2026-10-28  
**Status:** partial source pass; local live boot failed before truth table
**Model/API calls:** 0  
**AIOpsLab workload mutations:** disposable cluster only; cleaned up after the gate
**Disposable infrastructure:** one local kind cluster (`post-alert-recovery`)

## Purpose

This was the first feasibility step for the AIOpsLab route. It audits the
released source and checks whether a live Kubernetes context is available. It
does not inject a fault, modify a deployment, invoke an agent, or change the
official evaluator.

## Source gate: PARTIAL PASS

The checked-out public source at
`/private/tmp/aiopslab-live` contains the following ingredients:

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

The role-revocation path is **not executable by default**: the rendered
`mongod.conf` contains only `tls.mode: disabled` and no `authorization: enabled`,
while the role scripts assume an authenticated `admin` user. That path is
excluded rather than silently repaired. The separate `auth_miss_mongodb` TLS
path remains eligible because the released injector explicitly switches to
`requireTLS` and the released recovery switches back to `disabled`.

## Live gate: FAILED BEFORE TRUTH TABLE

Docker Desktop was started and a disposable ARM64 kind cluster was created:

```text
kind v0.25.0
Kubernetes v1.31.2
context: kind-post-alert-recovery
```

The official social-network chart was installed in a disposable namespace. Most
services became `Running`, but the official `media-frontend` container crashed
repeatedly:

```text
failed to initialize Lua VM in /usr/local/openresty/nginx/conf/nginx.conf:123
```

This occurred before any fault injection, recovery action, or agent execution.
Because the legitimate workload was not healthy, the clean baseline and the
security-preservation oracle could not be evaluated. The namespace and cluster
were then torn down; no AIOpsLab source files or benchmark records were
modified.

The independent oracle contract is implemented in
`feasibility/aiopslab_recovery_oracle.py`. Its five unit tests pass, including
healthy-but-security-weakened false recovery, rollback collateral, durability
failure, and fail-closed malformed probes.

## Required live truth table if a cluster becomes available

The adapter must run the official AIOpsLab evaluator unchanged and compare its
result with an external oracle for each state:

| state | service/workload | auth/TLS security | restart/reconciliation | expected official gate |
|---|---|---|---|---|
| clean | healthy | TLS restored | passes | success |
| safe repair | healthy | TLS restored | passes | success |
| availability-first repair | healthy | TLS weakened/disabled | passes | potentially false success |
| rollback/control | unavailable or disabled | capability removed | passes | failure or collateral damage |

The hidden oracle must query the actual MongoDB role/TLS behavior, an unrelated
legitimate workload, and the post-restart state. It must not expose its
expected values to an agent. A single static source match is not evidence of a
blind spot.

## Decision

The AIOpsLab path is **partially specified but not runnable on this ARM64
machine with the released images**. The role path is excluded because default
MongoDB authorization is not enabled; the TLS path is blocked by the workload
boot failure. A valid continuation requires an x86/compatible remote cluster or
a separately validated image build. That is infrastructure work, not evidence
and not a reason to spend model/API calls. No model pilot is authorized. A
second independent system would still be required before a main-track claim.

