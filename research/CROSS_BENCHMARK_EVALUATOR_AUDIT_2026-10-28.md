# Cross-benchmark evaluator audit — 2026-10-28

## Status

This is a source-level, zero-model-call audit. It is **not** evidence that a
cross-benchmark blind spot exists. The intended paired-state test is gated on
first establishing that the released systems expose comparable recovery
evaluators.

## Audit question

Do post-incident/recovery benchmarks accept restoration of an observable
service while an independently checked security, authorization, or evidence
state remains weakened?

The proposed paired cases are:

* **preserved:** service works and the security/integrity invariant is restored;
* **weakened:** service works but the invariant is still weakened.

An evaluator blind spot would require the official evaluator to accept both,
while an independent probe rejects the weakened case.

## Released systems inspected

### AIOpsLab

Source: <https://github.com/microsoft/AIOpsLab>

The released app-fault tasks include real authentication-related faults:

* `revoke_auth` removes MongoDB admin privileges and has a corresponding
  recovery routine;
* `auth_miss_mongodb` changes MongoDB TLS/auth configuration and has a
  corresponding recovery routine.

However, the mitigation success predicate in the released task classes is:

```python
self.results["success"] = self.wait_until_pods_healthy(self.namespace)
```

`wait_until_pods_healthy` checks container readiness, crash-looping, and
termination. It does not query the MongoDB role, TLS setting, API authorization,
or an evidence/integrity invariant. This makes AIOpsLab a genuine candidate
for the paired-state test: a healthy namespace can be accepted even if a
security property is wrong, provided the workload still starts.

This is a **candidate evaluator weakness**, not yet a measured result. A live
paired run would require a working Kubernetes deployment and must be done with
the official evaluator unchanged plus an external security probe.

### CUA-Recovery

Source: <https://github.com/xu-hu-2002/CUA-Recovery>

The public evaluator is materially different. It combines:

* rubric-based task success, where every criterion must be satisfied;
* state probes and state fingerprints;
* replay/provenance checks;
* Pass@3 aggregation.

The default released environment probes SQLite database digests and hashes of
files under Desktop/Documents/Downloads. The default probe configuration does
not include an authorization, credential, service-permission, or evidence
preservation invariant. Therefore the system is potentially blind to those
properties **only when a task's expected state also omits them**.

But the public release does not provide a ready-made security-preservation
task with the required paired states. Adding one would be a new benchmark
construction, not a faithful audit of an existing released case. CUA-Recovery
therefore cannot currently count as a second independent paired-state result.

### SecRespond

Source: <https://arxiv.org/abs/2607.26791> and
<https://huggingface.co/datasets/Alibaba-NLP/SecRespond>

SecRespond evaluates five written reports, including a remediation plan. Its
official evaluation skill scores detection (discovery, evidence, attribution)
and plan quality (correctness, completeness), with explicit checks for
remediation verification and business impact.

This is not a live recovery evaluator: the released range is a read-only
forensic disk snapshot plus alert/security-product artifacts, and the judge
scores the agent's reports. It does not execute a proposed repair, restart a
service, or independently probe post-repair authorization/evidence state.

Consequently, a service-restored/security-weakened pair cannot be run through
the official SecRespond evaluator without creating a new altered range and
changing the object being benchmarked. SecRespond is adjacent evidence, not a
valid second paired-state replication for this audit.

## Gate result

The cross-benchmark claim is **not established**. At present:

* AIOpsLab exposes a plausible service-health-only mitigation gate;
* CUA-Recovery exposes configurable state/rubric checks but no released
  security-preservation pair;
* SecRespond evaluates written forensic/remediation reports rather than live
  repaired state.

This is a comparability failure, not a publishable phenomenon. We must not
pool these systems and call the differences a common blind spot.

## Advancement rule

Proceed to implementation only if we can identify **two independently released
systems that both provide executable, unchanged recovery evaluators** and can
accept the same preserved/weakened paired states without constructing a new
benchmark task. Otherwise close this line as a careful evaluator/substrate
audit and do not spend model/API calls.

