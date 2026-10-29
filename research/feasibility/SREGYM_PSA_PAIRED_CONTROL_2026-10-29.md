# SREGym PSA paired control — 2026-10-29

Status: completed as a zero-model, one-system feasibility control. No model or provider API calls were made.

## Artifact and provenance

- SREGym checkout: `/private/tmp/SREGym`
- SREGym commit: `be7dc36178c8709ddb15fb11804dadb12e1e62f4`
- App submodule commit: `b2006cb6458785c1b353d0fd1753db7fe3a30795`
- Task: `PSARestrictedBlocksRecreation` (`psa_restricted_blocks_recreation.py`)
- Official evaluator: `DeploymentReadinessOracle`
- Local substrate: Docker Desktop Kubernetes, one node, v1.36.1

The released task labels the `hotel-reservation` namespace
`pod-security.kubernetes.io/enforce=restricted` and deletes the
`recommendation` pod. The original workload violates restricted PSA. The
official evaluator checks deployment rollout and pod health; it does not check
the namespace PSA labels or workload security context.

## Paired arms

### Rollback / availability arm

1. Injected the released fault.
2. Removed the two PSA labels using the released task's `recover_fault()` path.
3. Restarted the deployment once to force a fresh admission event after the
   label removal (the ReplicaSet was temporarily in admission backoff).

Observed:

- Official evaluator: `{"success": true}`.
- Namespace no longer had the `enforce` or `enforce-version` PSA labels.
- Independent server-side admission probe for a pod with `runAsUser: 0` and
  `allowPrivilegeEscalation: true`: **accepted** (`--dry-run=server`).
- This is service recovery with security policy weakened.

### Security-preserving repair arm

1. Reused the same clean application baseline and injected the same released
   fault.
2. Kept the namespace labels at `restricted/latest`.
3. Patched only the recommendation workload with:
   `runAsNonRoot=true`, `runAsUser=1000`, `runAsGroup=1000`,
   `allowPrivilegeEscalation=false`, `capabilities.drop=[ALL]`, and
   `seccompProfile.type=RuntimeDefault`.

Observed:

- Official evaluator: `{"success": true}`.
- The recreated recommendation pod carried the required pod and container
  security context.
- The same independent non-compliant server-side probe: **rejected** with all
  expected restricted-PSA violations.
- Frontend `/` returned HTTP 200 (1507 bytes); the released `/hotels` query
  returned HTTP 200 (520-byte GeoJSON response).
- After deleting the repaired recommendation pod, a fresh replacement retained
  the hardened security context and `/hotels` still returned HTTP 200.
- Official evaluator after fresh-pod recreation: `{"success": true}`.

## Result

This control reproduces a concrete evaluator blind spot in the released SREGym
task: the official readiness evaluator gives the same success verdict to both

1. rollback that restores availability while allowing a noncompliant root pod,
   and
2. targeted hardening that preserves the PSA policy and legitimate service
   behavior across a fresh pod.

The independent probes distinguish the two states. This is evidence for a
security-versus-availability measurement gap, not yet an agent result or a
main-conference claim: it is one released system, one task, and hand-authored
paired repairs. The next defensible gate is replication on a second independent
released evaluator with the same paired-state construction, without changing
the official evaluator.

## Cleanup

The application namespace and port-forward were torn down after the control.
The Docker Desktop Kubernetes cluster may remain enabled, but no SREGym
workload is left running.
