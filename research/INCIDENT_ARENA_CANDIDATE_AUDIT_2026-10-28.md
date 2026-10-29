# Incident Arena cross-system candidate audit — 2026-10-28

## Status

This is a source-level, zero-model-call audit of the public Incident Arena
release at commit `fba011e451653c4058c2dc80a97c5d260c036872`. It identifies a
strong candidate for the second-system paired test, but it is **not yet a
measured evaluator-blind-spot result**.

## Why this candidate is materially different

Incident Arena is an independently released, executable SRE benchmark with 20
live tasks over Frappe, Saleor, and a Slack-like service. Task 014 is a
particularly good fit because its incident is not merely “make sends work”:

* the user instruction says a mandated `read_consistency_strict` compliance
  window is active and **must stay on**;
* the shipped oracle repairs the channel database-pool capacity and explicitly
  leaves the compliance window enabled;
* the task runs a sustained traffic soak and checks state survival, restart /
  boundary evidence, and repair scope.

The task therefore contains a real availability-versus-policy constraint in the
released artifact, rather than one invented by this project.

## What the official evaluator actually checks

The task's `ground-truth.yaml` and `tests/test.sh`/`tests/verifier/` enforce:

* sustained latency, error rate, goodput, and send-lane health;
* required services running and traffic reconciliation;
* changed-key scope limited to the two channel-pool keys;
* channel-pool capacity floors and ceilings at declaration and soak end;
* PostgreSQL scope and protected-data survival;
* an agent-free verifier boundary and evidence-bundle binding.

The compliance event is not represented in the repair-scope key set or in the
task's protected challenge. A repository-wide search of task 014 finds no
`protected_events`/`strict_mode_inactive` check. The only event references in
the task are the timed fault injection in `task.values.yaml` and comments in
the oracle explaining that the event should remain active.

This omission is not universal across Incident Arena: task 011, for example,
does ship explicit verifier checks for affected events being inactive. That
within-release contrast makes task 014 a useful controlled candidate rather
than a generic accusation about the benchmark.

## The paired test and the confound that kills it

The apparent pair would have been:

1. **Policy-preserving arm:** execute the shipped oracle. It restores the
   channel pool to 20/10 and leaves `read_consistency_strict` active.
2. **Policy-weakened arm:** execute the same pool repair, then deactivate the
   runtime compliance event through the task's existing `/admin/event` control.

That pair is **not valid in the released task**. `environment/task.values.yaml`
contains a second `admin_event` with `anchor: declaration`, which reactivates
`read_consistency_strict` immediately when the agent hands the episode back.
Therefore a pre-declaration event-off shortcut is repaired by the task generator
itself before the verifier's final state is collected. A post-declaration edit
would require mutating the system after the terminal agent boundary and would
not be a legitimate agent recovery arm.

This is exactly the kind of temporal confound the cross-system gate is intended
to catch: the source-level omission of an event-preservation check does not
yield an observable weakened final state. No Incident Arena blind-spot result
is claimed.

## Current execution constraint

The public release requires Harbor plus a Linux/k3s-style Docker environment;
the task README specifies roughly 8 CPUs, 16 GB RAM, and 40–77 GB storage per
task. The current local machine has about 19 GB free and no Harbor installation,
so launching the environment locally would be an unsafe and non-reproducible
attempt. No model calls, API calls, or task runs were made in this audit.

## Gate decision

**Candidate fails the paired-state gate and this branch is closed.** Incident
Arena is a genuine independent released recovery system, but task 014's
declaration-anchored re-trigger prevents the required policy-weakened state
from surviving to official verification. Running it would spend substantial
compute without testing the claimed comparison. The AIOpsLab result remains a
single-system evaluator audit; no cross-system claim should be made from this
candidate.

