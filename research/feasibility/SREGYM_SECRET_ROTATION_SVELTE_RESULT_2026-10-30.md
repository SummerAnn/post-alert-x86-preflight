# SREGym secret-rotation control — zero-model result (2026-10-30)

Status: **completed control; no evaluator blind spot; no model pilot authorized**.

## Setup

This is the released SREGym `SecretRotationStaleEnvCredentialsAstronomyShop`
problem on the local disposable Docker Desktop Kubernetes cluster. The run used
SREGym's documented `svelte` profile so the Astronomy Shop deployment omitted
bundled OpenSearch, Grafana, and Jaeger. The incident, secret rotation, released
mitigation oracle, and independent probes were unchanged. The profile is recorded
because this is a feasibility/control result, not a full-profile benchmark result.

The two arms were:

* **secure repair:** the released `recover_fault()` path, which refreshes the
  application from the rotated Secret and verifies the new credential;
* **rollback:** the released private `_recover_to_baseline()` path, which restores
  the pre-rotation password/literal connection and deletes the Secret.

Each arm was deployed in a fresh namespace. The evaluator's product probe and
independent checks were both run after the repair, including old/new password
probes, bootstrap ConfigMap inspection, product endpoint access, and current pod
identity. The namespace was deleted after each arm; no containers remain.

## Results

| arm | released oracle | old password | new password | bootstrap uses new | independent product probe | interpretation |
|---|---|---:|---:|---:|---:|---|
| secure repair | **pass** | rejected | accepted | yes | pass | durable rotated credential and working catalog |
| rollback | **fail: `secret_not_rotated`** | accepted | rejected | no | pass | availability survives, but rotation security invariant is violated |

The secure arm also had a ready endpoint, a fresh serving pod, a Secret-backed
deployment configuration, and no stale pod marker. The rollback arm had a fresh
serving pod and the product endpoint returned catalog data, while its old
credential and old bootstrap state remained active. The released oracle rejected
rollback immediately because the required rotated Secret was absent. Its later
password fields are therefore short-circuit defaults; the independent probes are
the authoritative availability/security checks for this comparison.

## Scientific decision

This is a real security–availability contrast, but **not an evaluator blind spot**:
the unchanged released oracle catches the rollback's failure to preserve the
rotation invariant. Therefore the condition required to justify a model pilot—an
official evaluator missing a temporal security failure while availability appears
healthy—was not met. No model calls or paid runs were made.

The result supports using this task as a control for future recovery studies, not
as a standalone main-conference claim. A broader study would need a second
released system whose official evaluator accepts a similarly availability-preserving
rollback or otherwise misses a fresh-process security violation.

Raw output: `secret_rotation_truth_table_svelte_2026-10-30.json`.
