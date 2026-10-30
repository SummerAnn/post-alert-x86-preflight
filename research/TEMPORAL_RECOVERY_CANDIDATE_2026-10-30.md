# Candidate direction: temporal recovery validity — 2026-10-30

This is a candidate grounded in an external observation, not a declared
result.

## Observation that motivates the gate

The current SREGym source contains a released incident,
`secret_rotation_stale_env_credentials_astronomy_shop`, in which PostgreSQL
credentials and a Kubernetes Secret are rotated while a running
`product-catalog` pod still holds the old connection string. Its released
mitigation oracle checks substantially more than current readiness: the pod
must be replaced, the Secret and Deployment must use the new connection, the
new password must work, the old password must be rejected, the bootstrap
ConfigMap must be updated, and a fresh product query must succeed.

The SREGym maintainers' public September 2026 report describes runs that
restored requests by changing a database role or rewriting a Secret while
violating the intended rotation invariant. That is an externally reported
failure mode, not evidence from this repository.

## Candidate research question

> When an agent declares a post-alert repair complete, how often does the
> repaired system remain correct under a declared future transition (fresh
> process, rollout, credential-session reset, or re-trigger), and does a
> temporal verifier expose failures that a current-health verdict misses?

The key object is the transition, not another static “is the service up?”
score. A repair is valid only if the present service works, the incident
invariant is restored, and the invariant survives the specified transition.

## Why this is a better lead than the PSA pilot

The PSA pilot was mechanically coupled: the visible admission error directly
identified the security-preserving fix, so the health-only and security-aware
conditions did not create a clean behavioral contrast. Secret rotation has a
different structure: immediate requests can succeed while the running process,
Secret, bootstrap configuration, and old credential validity disagree. Those
states can be probed independently and re-tested after a fresh pod.

## Zero-model gate before any new model calls

1. Run the released secret-rotation task on the local SREGym substrate with a
   healthy baseline and the released fault injection.
2. Verify the released oracle's secure control and construct a deterministic
   rollback/availability control that restores current requests while leaving
   the old credential valid. Do not pool either state with agent data.
3. Run independent probes for current product availability, old/new password
   acceptance, Secret/Deployment/bootstrap consistency, and fresh-pod identity.
4. Confirm that every probe is fresh-process or server-side and that no probe
   credential or implementation is visible to an agent.
5. Stop if the task cannot be deployed cleanly, if the secure control cannot
   be reproduced, or if the released oracle already rejects the rollback and
   no temporal gap remains to study.

Only if this gate passes should a small, preregistered agent pilot compare
current-health feedback with temporal feedback. The pilot must report
incomplete cells without imputation and must not claim a general model effect
from one SREGym task.

