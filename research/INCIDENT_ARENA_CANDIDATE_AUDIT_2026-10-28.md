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

## The paired test to run (not run yet)

Use the task's released environment, runner, and verifier unchanged:

1. **Policy-preserving arm:** execute the shipped oracle. It restores the
   channel pool to 20/10 and leaves `read_consistency_strict` active.
2. **Policy-weakened arm:** execute the same pool repair, then deactivate the
   runtime compliance event through the task's existing `/admin/event` control.
   The official verifier should see the same healthy service, capacity, data,
   and evidence state; an independent post-run probe should observe that the
   mandated policy is off.

The second arm is a valid negative control only if it passes the official
verifier while failing the independent policy probe. Until that live result is
obtained, this document makes no claim that the verifier accepts the weakened
state.

## Current execution constraint

The public release requires Harbor plus a Linux/k3s-style Docker environment;
the task README specifies roughly 8 CPUs, 16 GB RAM, and 40–77 GB storage per
task. The current local machine has about 19 GB free and no Harbor installation,
so launching the environment locally would be an unsafe and non-reproducible
attempt. No model calls, API calls, or task runs were made in this audit.

## Gate decision

**Candidate passes the source gate; live replication is pending.** This is the
first independent released system found that plausibly supports the exact
secure-versus-policy-weakened comparison without constructing a new benchmark
task. If the paired run reproduces, the project has a defensible
cross-system finding. If it does not, this branch closes as a source-level
near miss.

