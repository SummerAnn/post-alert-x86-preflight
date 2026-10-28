# Substrate contract audit

**Date:** 2026-10-28  
**Status:** read-only candidate audit; no model/API calls  
**Research question held fixed:**

> After an alert, can an agent durably remove a harmful capability while
> preserving the legitimate function and relevant evidence/state?

This audit compares every currently available artifact or public substrate
against one contract. It does not change prompts, repair code, evaluator code,
or prior records.

## Admission contract

A candidate is admissible for a recovery experiment only if an evaluator
outside the agent workspace can independently check all of the following:

1. a real executable harmful capability, not only a text label or report;
2. a legitimate function that must remain usable;
3. a rollback/availability-first control that can remove the capability while
   causing measurable collateral damage;
4. a hidden probe unavailable to the agent that tests the capability;
5. a fresh-process, restart, or declared reconciliation event for durability;
6. preservation of unrelated state/evidence, with fail-closed checks;
7. raw state and action traces retained for audit;
8. an independent artifact or mechanism, rather than repeated copies of one
   reconstructed workspace.

Failure of any item is a reason to stop model calls for that candidate. A
candidate can still be useful as a control or evaluator-calibration artifact,
but it cannot support a broad recovery claim.

## Matrix

| Candidate | Capability + legitimate function | Rollback / hidden probe / durability | Preservation + provenance | Decision |
|---|---|---|---|---|
| **Incident-reporter replay** | Archived API-key exfiltration is executable; normal message sending is the legitimate path. | Rollback disables sending; targeted repair preserves sending. Capability probing is external. Fresh-process checking is present but no independently demonstrated dormant reactivation event. | Useful evaluator separation, but reconstructed archive and one mechanism. | **Calibration only; not a held-out result.** |
| **Expense-tracker durable enrichment** | Remote enrichment leaks a key and writes a cache; export/enrichment is legitimate. | Rollback disables enrichment; targeted repair redirects the endpoint and retains the cache. Fresh processes observe the durable cache. | Strongest internal durability feasibility, but one reconstructed artifact/model and no independent mechanism family. | **Calibration only; not enough for main-track evidence.** |
| **Remote-config validator** | Active remote fetch/cache path is executable; normal validation/summary is legitimate. | Rollback disables the fetch; targeted repair and fresh-process checks exist. | Corrected zero-model controls, but archive-reconstructed and one mechanism. Multi-agent pilot is ceiling (3/3). | **Evaluator test case; stop model study here.** |
| **Monitoring/telemetry artifact** | Pilot ledger describes a telemetry-context leak and repair/rollback arms. | Claimed controls exist, but raw observations and complete independent traces are not retained in this repository. | Feasibility ledger only; no auditable held-out evidence. | **Not admissible until raw evidence is recovered.** |
| **Compliance disclosure v2** | API-key header leak and report delivery are executable/legitimate. | Hidden loopback capture and fresh-process truth table work; rollback disables delivery. | No second persistence path, no durable reactivation, and targeted repair is one-line header deletion. | **Closed before model calls.** |
| **AIOpsLab MongoDB auth/TLS faults** | Real stateful Kubernetes/MongoDB faults: role revocation and TLS configuration changes; service availability is legitimate. | Released evaluator checks pod health only. It does not probe role scope, authentication, TLS, unrelated data, or restart/reconciliation durability. | Public, real substrate, but security-preservation adapter and paired states do not exist. | **Best external feasibility lead, not evidence. Zero-model adapter required before any pilot.** |
| **CUA-Recovery** | Real GUI recovery tasks and state fingerprints; default tasks are erroneous-state recovery, not security-capability removal. | Verification checks SQLite/file fingerprints. No security/auth/permission capability probe or preservation invariant is in the released default contract. | Large human-verified set, but a security pair would be newly authored. | **Not a direct substrate; new task construction required.** |
| **SecRespond** | Forensic alerts and response planning, but the released evaluator scores written detection/plan reports. | No live repair, restart, capability probe, or legitimate-function execution. | Useful comparison for response quality, not executable recovery. | **Ineligible for this experiment.** |
| **Recovery-Bench** | Recovery agents replay failed commands in fresh Docker tasks; some task names are security-adjacent. | Generic task reward; no declared hidden security capability, preservation function, or durable security invariant. LFS artifacts were not available in the audit checkout. | Task suite is not a paired security-preservation benchmark. | **Requires a new security task and evaluator.** |
| **AI SRE Arena** | Public Kubernetes incident/answer-key benchmark. | Explicitly reports mitigation/readiness proposals; no repair execution or recovery verification. | No executable post-alert recovery oracle. | **Ineligible for this question.** |

## What “try all” establishes

The candidates do not form one ready-made benchmark. They split into three
classes:

### 1. Three usable internal calibration artifacts

Incident-reporter, expense-tracker, and remote-config can exercise the
independent evaluator and demonstrate that targeted repair and rollback are
different operations. They are not independent mechanisms in the statistical
sense: they are reconstructed archive cases, selected for feasibility, and
mostly easy or ceiling-level under existing pilots. Repeating them would add
precision to infrastructure checks, not a main-track finding.

### 2. One real external lead, but no evidence yet

AIOpsLab is the only audited public system that already has stateful,
application-level auth/TLS faults and real service recovery. Its released
success criterion is availability-only, so it is a plausible place to test the
security-versus-availability mismatch. That mismatch is a **hypothesis about
the evaluator**, not a result. It requires an independent hidden security
oracle, paired safe/unsafe repairs, and a live zero-model truth table first.

### 3. Everything else needs a new benchmark

CUA-Recovery and Recovery-Bench would require authoring security-preservation
tasks and evaluators. SecRespond and AI SRE Arena do not execute repair. The
compliance artifact fails the difficulty contract. These are not quick
additional rows for the current experiment.

## Confound audit

The same failure patterns recur across the candidates:

* **Availability-only scoring:** a healthy service or completed task can hide a
  weakened security control (AIOpsLab, AI-SRE-style evaluators).
* **No hidden oracle:** if the agent sees the probe or rubric, the task measures
  instruction following rather than recovery (the earlier internal studies).
* **Rollback is not a repair baseline:** disabling a feature can look secure
  while destroying the legitimate function.
* **No durability event:** checking the immediate process misses cron/cache/
  database/configuration reactivation.
* **Reconstruction and selection:** archive-derived artifacts are not a random
  incident sample; successful, recoverable cases are overrepresented.
* **Single mechanism masquerading as replication:** multiple users, reps, or
  workflow roles inside one workspace do not create independent attack
  mechanisms.
* **Evaluator drift:** old result rows cannot be pooled when the command,
  schema, or expected state changed.

## Result and next gate

The research question remains viable, but “try every artifact we have” does
not produce a valid main-conference experiment. It produces one defensible
next gate:

> Build no model pilot. Implement one independent AIOpsLab adapter for the
> MongoDB-auth task, with a hidden role/auth/TLS oracle, a legitimate-workload
> probe, a restart/reconciliation check, and safe/unsafe repair truth-table
> controls. Stop if the adapter cannot distinguish those states or if a second
> independent system cannot be obtained.

If that gate passes, the next experiment must include AIOpsLab plus a second
independently implemented application, with the evaluator frozen before model
outcomes. If it fails, the honest output is an evaluator/infrastructure
feasibility paper or closure of this line—not another prompt or model batch.

## Sources in this repository

* `research/EVIDENCE_INVENTORY_2026-10-28.md`
* `research/INDEPENDENT_RECOVERY_ORACLE_SPEC_2026-10-28.md`
* `research/AIOPSLAB_SUBSTRATE_FEASIBILITY_2026-10-28.md`
* `research/EXTERNAL_SUBSTRATE_AUDIT_2026-10-28.md`
* `research/CROSS_BENCHMARK_EVALUATOR_AUDIT_2026-10-28.md`
* `research/COMPLIANCE_RECOVERY_V2_GATE_RESULT_2026-10-28.md`

