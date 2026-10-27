# Five candidate task designs — zero-cost comparison

Each candidate uses the same abstract incident: an agent made a change, an
alert arrives, and a successor responder receives tools plus fragmented
evidence. These are design sketches only.

## A. Containment completeness

**Manipulation:** one incident leaves two independent capability paths: a
visible credential and an external scheduled-state path. The alert names only
the visible path.

**Measure:** current capability after response, durability after a restart or
scheduled event, legitimate functionality, and collateral changes.

**Distinctive prediction:** removing the named path is often insufficient;
closure requires testing the residual path.

**Main risk:** this is close to SecRespond and the retired recovery study.
Reject unless the two-path design changes a published benchmark conclusion or
reveals a reproducible closure error not measured there.

## B. Responder state reconstruction

**Manipulation:** distribute causal evidence across agent trace, credential
inventory, host state, and service logs. Give the successor only a subset or a
structured handoff.

**Measure:** reconstruction of affected assets, causal sequence, uncertainty,
and residual capability before any mutation.

**Distinctive prediction:** final repair can be correct while scope or
uncertainty reconstruction is wrong.

**Main risk:** generic handoff and persistent-state benchmarks may already
measure state recovery. Require incident-specific causal scope and uncertainty
as the differentiator.

## C. Evidence-preserving response

**Manipulation:** the easiest containment action deletes or overwrites evidence;
an alternative action contains the capability while preserving an immutable
copy.

**Measure:** containment success, evidence retention, later attribution/scope
reconstruction, and collateral impact.

**Distinctive prediction:** agents optimize immediate containment and sometimes
destroy information needed to establish whether containment was complete.

**Main risk:** ordinary forensic-response work already values preservation.
The contribution must be an agent-specific tradeoff with executable scoring,
not a generic checklist.

## D. Agent-to-agent recovery handoff

**Manipulation:** detection agent and responder are different agents. Vary the
handoff: raw trace, compressed summary, structured incident record, or summary
with explicit uncertainty and persistence inventory.

**Measure:** successor reconstruction, safe containment, evidence retention,
and closure calibration.

**Distinctive prediction:** summaries that preserve task state but omit
uncertainty or residual paths produce unsafe closure.

**Main risk:** handoff benchmarks are already numerous. The incident-response
state and closure tests must be essential, not decorative.

## E. Closure under uncertainty

**Manipulation:** vary whether the evidence permits proof of complete recovery.
Require the responder to choose resume, hold, or escalate.

**Measure:** safe resume, justified hold/escalation, false reassurance,
unnecessary shutdown, and evidence quality.

**Distinctive prediction:** agents resume after plausible repair without enough
evidence to justify closure.

**Main risk:** overlaps with verification and incident-response benchmarks.
The novelty would require calibrated asymmetric-cost decisions, not merely a
postcondition check.

## Common rejection criteria

Reject a candidate if its only outcome is final task success, if the hidden
truth is recoverable from one obvious file, if the scorer conflates repair with
verification, or if the same manipulation is already a standard condition in
the closest benchmark.

## Current ranking after design

1. Evidence-preserving response — most distinctive if executable and causal.
2. Responder state reconstruction — strongest fit to multi-agent safety.
3. Closure under uncertainty — important but crowded.
4. Agent-to-agent recovery handoff — relevant but crowded.
5. Containment completeness — important but closest to existing work.

This ranking is provisional and does not authorize model calls.
