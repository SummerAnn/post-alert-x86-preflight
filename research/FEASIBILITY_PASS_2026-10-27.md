# Five-candidate feasibility pass — 2026-10-27

This pass used repository artifacts only. No model calls were made and no old
run was reclassified as new evidence.

## Deterministic support already available

The archived project contains independent score fields for reconstruction,
state repair, preservation, downstream continuation, validation, closure, and
harmful actions. It also contains trace-level evidence and hidden-world
oracles. Therefore all five candidate designs are technically scoreable.

## Feasibility results

| Candidate | Can score distinct outcome? | Main confound | Status |
|---|---:|---|---|
| Containment completeness | Yes | overlaps old external-state recovery study | **Needs new mechanism** |
| Responder state reconstruction | Yes | generic handoff/state benchmarks | **Promising** |
| Evidence-preserving response | Yes | preservation must affect later reconstruction, not just file count | **Most promising** |
| Agent-to-agent handoff | Yes | crowded handoff benchmarks | **Promising with incident-specific state** |
| Closure under uncertainty | Yes | ordinary postcondition verification | **Needs asymmetric-cost decision task** |

## What the archive does and does not establish

The archive proves that the harness can separately record many relevant
dimensions. It does not establish a new effect for any candidate. Existing
traces are development history, not a new confirmatory sample.

## Required next gate

Before model calls, construct one deterministic paired case for the top three
(state reconstruction, evidence preservation, and handoff):

- same incident and same ground truth;
- one controlled manipulation per candidate;
- independent scores for diagnosis, repair, evidence retention, and closure;
- a later task that makes evidence loss or handoff omission consequential;
- an adversarial scorer test showing that the easy action cannot fake success.

If any candidate cannot produce a distinct score without borrowing the same
manipulation, drop it. Only then should a small pilot be considered.

## Decision

The five candidates are not five experiments to launch. They are five designs
to reduce to three deterministic paired cases, then one model pilot. The
current evidence supports design work, not a scientific claim.
