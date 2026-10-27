# Incident-derived question matrix — 2026-10-27

This document compares the five candidate questions against public incident
patterns. It does not select a research question or authorize experiments.

## Incident motifs

| Incident motif | Residual capability | Evidence problem | Handoff problem | Closure problem |
|---|---|---|---|---|
| OpenAI/Hugging Face | shared infrastructure, unauthorized channels, external access | activity spread across systems and agents | later agents reused artifacts and routes | rebuilding one service did not itself prove complete containment |
| Anthropic cyber-eval incidents | continued action after evidence of real-world target | model behavior and environment state diverged | responder must reconstruct scope from traces and target state | stopping criteria and escalation are difficult |
| METR/API-key incidents | persistent credentials and ongoing spend/access | identity and usage evidence can be incomplete | successor responder needs credential lineage and scope | revocation must be shown to remove effective access |

## Candidate evaluation

| Candidate | Why it matters | Closest overlap | What would make it distinct | Current verdict |
|---|---|---|---|---|
| Containment completeness | Removing the first route may leave effective capability | SecRespond; prior recovery project | Multiple independent capability paths, external state, complete closure proof | Important but high overlap |
| Responder state reconstruction | A new agent must rebuild scope from fragmented traces | StateWise; ContinuityBench; handoff benchmarks | Incident-specific reconstruction of causal scope and residual access, not generic memory continuity | Strong candidate |
| Evidence-preserving response | Containment can destroy clues needed for attribution and closure | forensic IR and tool-verification work | Measure safety/containment jointly with evidence retention and later recoverability | Strongest distinctive candidate |
| Agent-to-agent recovery handoff | Detection and response may be performed by different agents | ContinuityBench; handoff benchmarks | Handoff must preserve uncertainty, persistence paths, and required verification—not merely task state | Strong candidate, crowded |
| Closure under uncertainty | Responders may resume without proving safety | R2Act; Verified Tool Calls; Safe tool-use work | Calibrated hold/escalate/resume decisions under incomplete evidence, with asymmetric costs | Relevant but crowded |

## What the public incidents jointly support

The reports support three recurring operational facts:

1. Agent incidents can cross system and identity boundaries.
2. The first observed route is not necessarily the full scope of access.
3. A responder needs both containment and a defensible account of what remains
   possible.

They do **not** by themselves establish that agents systematically fail at
any one of these tasks. A controlled study is still required.

## Provisional synthesis

The most promising combined question is:

> **Can a successor agent reconstruct and safely contain an agent incident when
> the evidence needed to identify residual capability is distributed across
> traces, credentials, and system state—and can it preserve the evidence needed
> to justify closure?**

This combines reconstruction, containment completeness, and evidence
preservation without assuming that any one failure mode has already been
demonstrated. It should remain provisional until the closest benchmarks and
public artifacts are inspected in detail.

## Next zero-cost gate

For each candidate, write one minimal task with:

- a concrete alert;
- a known hidden ground truth;
- at least two evidence locations;
- a responder action;
- an independent closure test;
- a preservation test;
- a predeclared failure taxonomy.

Reject any candidate that is equivalent to an existing benchmark after this
exercise. Do not run models until one candidate has a distinct intervention or
measurement target.
