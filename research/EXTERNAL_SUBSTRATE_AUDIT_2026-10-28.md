# External substrate and novelty audit (2026-10-28)

This is a read-only literature and source audit. No code, model calls, or
external benchmark runs were performed.

## Direct and adjacent occupancy

| external work | what it already establishes | implication for this project |
|---|---|---|
| [SecRespond](https://arxiv.org/abs/2607.26791) | Ten compromised cloud-host ranges, four entry-point types, 21 ATT&CK techniques, five operating systems, and 23 frontier models. It reports that agents find alert-exposed problems but miss silent persistence and produce incomplete/unverified remediation plans. | A generic post-compromise recovery benchmark is already occupied. A new paper cannot claim first measurement of investigation/remediation difficulty. |
| [AIOpsLab](https://github.com/microsoft/AIOpsLab) | A Microsoft framework with live microservice environments, fault/workload injection, telemetry, and evaluators for detection, localization, analysis, and mitigation. | It is a credible substrate for a new security-control task, but ordinary mitigation on AIOpsLab is not novel. Any extension must add a causal security phenomenon, not another fault. |
| [CUA-Recovery](https://github.com/xu-hu-2002/CUA-Recovery) | 2,250 human-verified persistent erroneous states over 100 tasks, takeover at six depths, and verifier-confirmed repair. | Hidden state errors and recovery after the cause leaves context are already benchmarked at scale. |
| [Stateful Agent Security Evaluation](https://github.com/junwenleong/stateful-agent-security-eval) | A 5,040-run persistent-memory security evaluation separating storage from later execution and analyzing defense layers. | Persistent state and delayed attack execution are already an active benchmark topic; this is adjacent to, but not the same as, post-alert repair. |
| [AIOpsDoom/AIOpsShield](https://arxiv.org/abs/2508.06394) | Telemetry manipulation can steer AIOps agents toward incorrect remediation; a sanitization defense is evaluated. | The control-integrity/observation-channel idea is not empty. A new version would need a distinct causal setup and independent probes. |
| [ColdStart](https://www.deaimer.com/benchmarks/coldstart) | A public benchmark page explicitly defines functional recovery, state safety, durability, integrity/security, evidence quality, and minimal-change scoring, with oracle, no-op, shortcut, restart, and audit checks. | This overlaps the exact difficulty contract developed here. It is a public benchmark description rather than a peer-reviewed result verified in this audit, but it makes the contract itself non-distinctive. |

## What remains potentially distinct

The only credible seam is not “can an agent repair a persistent incident?” That
is now directly covered. A possible new question would be:

> Can a responder safely remediate when the observation/control channel itself
> has been altered, while an independent behavioral probe remains trustworthy?

This is a causal control-integrity question, not ordinary recovery. It would
require all of the following in an existing runtime:

1. an effective security control whose behavior can change;
2. a monitor-visible configuration or trace that can remain apparently normal;
3. an independent probe that tests the real behavior;
4. a sham intervention and a defense that restores detection;
5. replication across at least two control types and two model families.

The current repository does not contain this substrate. AIOpsLab exposes
telemetry and mitigation, but using it for this question would require a new
security task and evaluator; it is not a zero-cost reuse of an existing result.

## Decision

Do not start another model pilot from the current repository. Do not rebrand the
existing recovery evaluator as a novel benchmark. If the project continues, the
next stage is a separate substrate feasibility audit of one open system such as
AIOpsLab, with no model calls, to answer only:

*Can an independently scored control-integrity task be implemented without
inventing an artificial exploit or copying SecRespond/AIOpsDoom?*

If the answer is no, close the post-alert-recovery line. If yes, it becomes a
new benchmark-construction project with a new preregistration—not a continuation
of the invalidated compliance or ceilinged multi-agent pilots.
