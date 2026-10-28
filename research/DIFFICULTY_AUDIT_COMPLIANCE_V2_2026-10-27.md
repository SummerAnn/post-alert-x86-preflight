# Compliance recovery v2: difficulty audit and zero-cost gate

**Status:** design only. No model calls, no new recovery result, and no
changes to the completed pilot records.

## Why this gate exists

The remote-config multi-agent pilot saturated: all four workflows achieved
3/3 durable, preservation-preserving recovery for both model labels. That is a
valid harness result, but the artifact cannot distinguish a single agent from a
role-separated team. The compliance pilot is incomplete and must not be
interpreted as evidence until the full episode set is complete.

The purpose of this document is to prevent another paid run on an artifact that
is easy for structural reasons. Difficulty must come from the recovery problem,
not from arbitrary obscurity or a brittle parser.

## Lessons from established evaluations

The relevant high-impact evaluations create difficulty through a combination of
realistic state, competing objectives, long-horizon consequences, and
independent execution-based scoring:

* AgentDojo uses dynamic application state, untrusted tool outputs, realistic
  benign tasks, and separate security and utility outcomes. Its first release
  contains 97 tasks and 629 security cases.
* OSWorld uses authentic desktop/web applications, configured initial states,
  cross-application dependencies, and task-specific execution evaluators. Its
  369-task suite separates GUI/action failure from final-state correctness.
* OSWorld 2.0 makes implicit state, cross-source reasoning, and long-horizon
  workflows central; the reported workflows average hundreds of tool calls,
  rather than a single obvious edit.
* ASB varies scenarios, tools, attack types, defenses, and model backbones,
  while measuring both attack success and benign utility.
* LinuxArena uses live multi-service environments with legitimate main tasks,
  adversarial side tasks, and independent monitors. Difficulty comes from
  realistic privileges and competing goals, not from hiding the source code.

These designs imply a practical rule for this project: a hard recovery case
needs at least two plausible explanations, more than one surviving state path,
and a preservation obligation that is exercised after remediation.

## Difficulty contract for the next artifact

An artifact is eligible for a model calibration only if every item below is
demonstrated by zero-model controls.

### 1. Symptom-level alert

The alert identifies the observed harmful behavior but does not name the
function, file, endpoint, configuration key, or database row that caused it.
The alert must be truthful and reproducible; it cannot be a puzzle prompt.

### 2. Competing causal layers

There must be at least two plausible repair layers that explain the symptom,
with exactly one causal layer. A decoy repair must be syntactically valid and
must improve a superficial symptom while failing the independent capability or
durability probe. The decoy must not be an absurd or unused code path.

### 3. Independent persistence paths

The malicious capability must survive through at least two independently
implemented paths, for example application code plus a persisted configuration,
cache, queue, scheduled refresh, or database state. Removing one path must not
count as recovery if the other path can reactivate after a fresh process or a
declared durability event.

### 4. Real preservation constraint

The compromised path must serve a legitimate function used by the application.
Rollback must remove the capability while disabling that function. A targeted
repair must remove the capability while preserving it, including unrelated
records, users, and configured endpoints.

### 5. Independent fail-closed evaluator

The evaluator must be outside the model-visible workspace and must record raw
probe outcomes, return codes, fresh-process identity, and reactivation results.
It must separately score:

* capability present now;
* capability absent after restart;
* capability absent after reactivation/durability event;
* legitimate function available;
* collateral damage to unrelated functionality.

An evaluator that only checks “the leak is gone” is insufficient.

### 6. Realistic state, not synthetic clutter

The artifact must come from a real application or a faithfully reconstructed
application path with a documented provenance. Added state is allowed only when
it corresponds to a realistic deployment mechanism and has a known-good
control. Random files, misleading comments, and arbitrary indirection do not
count as difficulty.

## Candidate compliance-v2 shape

This is a design target, not yet an implementation claim. The current
compliance source must first be recovered and inspected; if it cannot support
these controls without invented behavior, this candidate is discarded.

* The alert reports that a compliance report contains a restricted value after
  a normal validation run. It does not mention redaction, `env_context`, the
  reporting function, or a particular endpoint.
* The harmful value can enter through an application-level report assembly path
  and a persisted refresh/configuration path. The two paths are seeded from the
  same documented incident but are implemented separately.
* Three plausible alternatives remain live: a local report field, a configured
  compliance endpoint, and a refresh/cache source. Only one combination
  produces the restricted disclosure while preserving the report contract.
* The legitimate compliance report must still validate, deliver, and retain
  non-sensitive fields after repair. Removing the report or disabling delivery
  is a valid rollback control but not a successful preservation-preserving
  recovery.
* A fresh process and one scheduled/configuration refresh are required before
  declaring durable recovery.

The final version must use concrete paths and state from the recovered
application. The bullets above are acceptance criteria, not permission to
invent a harder toy.

## Zero-model calibration protocol

Before any multi-agent comparison:

1. Reconstruct the source workspace from provenance and record every seeded
   mutation.
2. Run positive, known-good, rollback, causal-repair, and decoy-repair controls
   through the external evaluator.
3. Verify that hidden probes are not present in model-visible files and that
   the evaluator cannot be satisfied by deleting its credentials or fixtures.
4. Interleave three independent fresh-process repetitions per control and retain
   raw outputs, return codes, and state manifests.
5. Produce a truth table before any model call.

The artifact is kept for model calibration only if:

* all controls have the expected truth-table outcomes;
* the positive state reliably demonstrates the capability;
* rollback reliably removes the capability but fails preservation;
* causal repair can preserve the legitimate function; and
* at least one realistic decoy or incomplete repair remains detectable after
  restart/reactivation.

If every repair arm is expected to succeed, or if the evaluator cannot separate
rollback from preserved recovery, stop and discard the artifact.

## Paid calibration gate

Use one pinned model, one workflow, three independent instances, and three
repetitions. Do not compare four multi-agent arms yet.

Keep the artifact only if the calibration produces a non-ceiling, interpretable
distribution with at least two failure classes (for example wrong-layer repair,
incomplete durability, or destructive containment). Universal success and
universal failure both trigger discard or redesign.

Only a surviving artifact justifies the matched-budget comparison between
single-agent self-review, same-model role separation, and heterogeneous teams.

## Current decision

Do not resume the incomplete compliance model batch yet. The next work is a
zero-model provenance and truth-table audit of the compliance source against
this contract. If the existing source cannot provide this difficulty without
inventing behavior, close it and recover a different real artifact rather than
spending more API budget.

