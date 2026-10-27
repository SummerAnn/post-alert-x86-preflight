# Literature review: post-alert recovery for persistent agent compromise

## Scope

This review asks what is already established about persistent compromise of LLM agents, incident-response agents, and automated security repair, and whether the current project has a defensible empirical gap.

## Closest work

### 1. Persistent attacks and carryover

**CarryoverBench** studies malicious instructions planted once into long-lived memory or scheduled tasks. It evaluates 101 tasks across 12 personal-assistant scenarios and measures whether the payload re-fires across later rounds. Its central result is persistence after the attacker leaves, not recovery after an alert. The paper therefore occupies the attack/persistence side of the problem, while leaving the post-alert eradication question open. [Xu et al., EMNLP 2026](https://aclanthology.org/2026.emnlp-main.1996/)

**Persistent-memory defense studies** evaluate where defenses sit in the architecture and whether delayed triggers remain effective. One large study evaluates six defenses across four layers and 5,040 runs on nine open-source models. This is a defense-at-injection/retrieval/execution study, not an agent-directed repair study. [Defense effectiveness across architectural layers](https://arxiv.org/abs/2605.08442)

**PersistBench** proposes longitudinal persistence, recovery-latency, utility-preservation, and trustworthy-forgetting metrics, with provenance tracking and replay. However, its documented scenarios are synthetic and its deterministic oracle backend is not a deployed agent. It is important adjacent infrastructure, and means that “we need metrics for persistence and retention” is not by itself novel. [PersistBench](https://github.com/Keerthi-Rapolu/PersistBench)

### 2. Post-compromise incident response

**SecRespond** is the closest benchmark by task framing. It gives agents a forensic disk snapshot plus alerts, scans, and baselines, and asks for forensic reports and remediation plans. Its headline result is that agents can address alerted problems more reliably than silent intrusions and do not achieve complete detection plus remediation on any range. The crucial distinction is that the primary deliverable is a report/plan evaluated from a snapshot; it is not a controlled test that the agent's repair removed a live capability while preserving legitimate functionality. [SecRespond](https://arxiv.org/abs/2607.26791)

**SIR-Bench** measures investigation depth and distinguishes genuine forensic investigation from alert parroting. This strengthens the case that finding the cause is a separate capability from reacting to the alert, but it does not evaluate executable containment or post-repair preservation. [SIR-Bench](https://arxiv.org/abs/2604.12040)

### 3. Recovery of persisted state

**Selective Revocation and Replay** is the most direct competing recovery result. It assumes suspicious roots are already known in a provenance-tracked text-only memory runtime, then selectively revokes descendants and replays writer events. In its narrow setting it reports zero residual attack success with retained benign state and lower recovery cost than rollback. This is a strong result, but it assumes explicit persisted state and known suspicious roots; it does not test an agent's ability to localize an unknown active capability in a real application or distinguish repair from destructive rollback. [Uyar, 2026](https://aliuyar.dev/research/selective-revocation-and-replay/)

### 4. Security patching and repair quality

SEC-bench, CVE-Bench, PatchEval, and PatchAgent evaluate vulnerability reproduction or patching, usually with exploit/PoC and regression tests. These establish that “security fix plus no regression” is a meaningful evaluation pattern, but they are pre-compromise software repair benchmarks. They do not model an already-running agent/application with residual attacker state, nor do they evaluate rollback versus surgical containment. [SEC-bench](https://papers.nips.cc/paper_files/paper/2025/hash/a9168f1c54e5147027f1e8cf83e1a775-Abstract-Conference.html), [CVE-Bench](https://aclanthology.org/2025.naacl-long.212/), [PatchEval](https://patcheval.github.io/), [PatchAgent](https://www.usenix.org/conference/usenixsecurity25/presentation/yu-zheng)

## What is already occupied

The following claims are not safe novelty claims:

1. Persistent state can outlive the attacker.
2. Delayed triggers and memory/scheduler channels are under-measured.
3. Agents struggle with silent intrusions and incident-response planning.
4. Recovery should measure residual attack success and utility retention.
5. Provenance-aware selective replay can outperform coarse rollback when the malicious root is known.

## The remaining credible seam

The literature leaves a narrower, testable question:

> **When an alert identifies a live post-compromise behavior in an application, can an autonomous repair agent remove the executable capability while preserving legitimate behavior, and how often does it choose destructive rollback or an incomplete patch?**

This is not a claim that agents are generally safe or that recovery is unsolved. It is an empirical comparison of three actions under the same active incident:

* **rollback/coarse containment:** remove or disable the affected feature;
* **targeted repair:** edit the vulnerable path to block the malicious behavior;
* **capability-guided repair:** provide an external live capability test and require repair plus verification.

Primary outcomes must be independently scored from runtime behavior:

* **eradication:** malicious capability absent after repair and after a restart/durability event;
* **preservation:** predeclared legitimate functionality still works;
* **collateral:** unrelated users, endpoints, or data paths remain functional;
* **evidence quality:** the agent's claimed fix matches the externally observed state.

The current two-artifact pilot (incident-reporting and expense-tracker applications reconstructed from ControlArena persistent-state logs) is only feasibility evidence. It shows that the harness can expose an active API-key exfiltration capability, and that both targeted and capability-guided repairs can remove it while retaining the intended command/export path. It does **not** yet establish a general model effect, because the sample is two artifacts and the arms were not powered for a paper claim.

## Go/no-go implication

The project should proceed only if it can expand the same evaluator to multiple independent artifacts and include a real rollback baseline. The paper-sized result would be a measured **security–availability tradeoff** or a reproducible failure mode (for example, agents pass the attack probe by disabling the feature, while surgical repairs have lower eradication or higher restart-survival failure). If all arms trivially pass on many artifacts, the project should stop rather than inflate a benchmark.

The current repo's strongest contribution is therefore not “post-alert recovery exists.” It is a possible **verified repair benchmark** whose unit of success is *live capability eradication plus preserved service behavior*, with explicit separation between known-root recovery and agent localization.

