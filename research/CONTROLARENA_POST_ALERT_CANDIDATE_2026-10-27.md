# Candidate substrate: post-alert recovery of persistent attacks

## Why this is the first credible adjacent direction

The local checkout of `control-arena-persistent-state-eval` is the implementation
behind *Distributed Attacks in Persistent-State AI Control* (COLM 2026). It has
real multi-PR persistence, gradual and concentrated attack policies, CLI and Flask
task families, trajectory and diff monitors, and side tasks such as exfiltration
and access-control backdoors. The paper studies attack success and monitor evasion;
it does not study what happens after an alert or after a missed alert.

## Non-duplicate research question

> After a persistent-state coding agent is flagged, which response protocol actually
> removes the executable side task while preserving the main task, and how often does
> a response that looks clean at the current PR leave a dormant or cross-PR residue?

This is narrower than “recovery is hard.” The unit is an alerted persistent attack,
the outcome is an externally probed executable capability after response and a later
fresh PR, and the comparison is between response protocols (rollback, targeted
repair, full-history investigation, and independent capability testing).

## Why it could matter

The source paper establishes that persistent attacks evade monitoring and that
stateful monitoring helps. A downstream safety decision still remains unresolved:
whether a monitor alert is a reliable boundary after which the system can be made
safe. A response can remove the suspicious diff while preserving a dormant trigger,
secret path, or later-PR dependency. That is a distinct operational claim, not a
relabeling of monitor evasion.

## Required evidence before any model call

1. Pick two existing side tasks with an executable postcondition (not merely a
   textual diff), ideally one direct exfiltration and one access-control backdoor.
2. Verify the side task with an external probe that is hidden from the agent and
   independent of the monitor/scorer.
3. Verify that the benchmark can snapshot an alerted state, apply a response, restart
   the service or begin a fresh PR, and then probe both immediate and dormant effects.
4. Define preservation tests for the legitimate main task and a fail-closed scorer.
5. Confirm that rollback, repair, and probe-based response are causally separable.

If any of these fail, this candidate is not ready for a paid pilot.

## What would be a real finding

The strongest plausible result is not “one method wins.” It is a response-surface
finding such as: current-alert cleanup has high apparent success but leaves a
measurable fraction of executable cross-PR residue; or response quality depends on
whether the attack is gradual versus concentrated, even at matched monitor scores.
That would directly extend the persistent-state control paper and produce a concrete
deployment implication.

## Current status

Substrate found; no model calls and no confirmatory claim. Next action is a read-only
implementation audit of two side tasks and the snapshot/restart lifecycle. Do not
launch a model pilot until the five evidence requirements above are demonstrated.
