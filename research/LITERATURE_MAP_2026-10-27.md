# Literature map — 2026-10-27

This is a scouting map, not a novelty claim. The papers below are the closest
verified matches found in the first search pass.

## Closest overlaps

### Direct post-incident recovery

- **SecRespond** evaluates LLM agents on post-compromise incident response.
  This occupies the broad cyber-recovery benchmark space.
  <https://arxiv.org/abs/2607.26791>
- **R2Act** evaluates diagnosis-to-recovery action selection on 302
  quality-audited Kubernetes incidents. It explicitly separates diagnosis,
  action, and health verification.
  <https://arxiv.org/abs/2607.04623>
- **ColdStart** claims a benchmark for recovery of unfamiliar broken systems,
  including integrity, durability, evidence quality, and minimal change.
  <https://www.deaimer.com/benchmarks/coldstart>

### Verification and recovery

- **Verified Tool Calls** studies postcondition checks, retries, idempotency,
  and non-atomic tool failures. It is close to the closure/verification axis,
  but assumes the verification wrapper is available.
  <https://arxiv.org/abs/2608.02645>
- **Real-Time Detection and Repair of LLM Agent Failures** detects failures and
  triggers repair using telemetry and deterministic verification.
  <https://arxiv.org/abs/2608.02464>
- **ToolMisuseBench** evaluates recovery after runtime tool misuse with typed
  failure and recoverability metadata.
  <https://aclanthology.org/2026.realm-1.28/>

### Persistent state and handoff

- **StateWise** studies diagnosing and repairing persistent operational state
  before later agent actions, including evidence grounding and repair lineage.
  <https://arxiv.org/abs/2610.05241>
- **ContinuityBench** evaluates recovery after interrupted work and compares
  transcript, memory, and handoff representations.
  <https://openreview.net/pdf?id=3N3BzvoLbG>
- **AI Handoff Continuity Benchmark** measures exact state recovery across
  handoffs. It is relevant to the multi-agent extension, but not specifically
  to post-alert remediation.
  <https://handover.sh/benchmark>

## Preliminary gap assessment

The generic claim "agents need to detect, repair, and verify failures" is
already occupied. A new project must therefore contribute a sharper axis, such
as a controlled distinction between:

1. diagnosis of the alert;
2. selection and execution of the repair;
3. independent proof that the repair worked;
4. preservation of valid state and evidence lineage.

The most promising possible gap is not yet a claim: whether post-alert recovery
fails specifically when the alert, repair target, and verification surface are
different state boundaries, especially when a successor agent inherits only a
partial operational record. This needs a fresh audit against the papers above
before any experiment is designed.

## Immediate rule

No paid run until one candidate question survives a paper-by-paper comparison,
has a concrete observable failure, and is not reducible to an existing
diagnosis/action/verification benchmark.
