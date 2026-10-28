# Independent Recovery Oracle — design note (2026-10-28)

## Why this exists

The released benchmarks inspected so far do not expose one comparable recovery
evaluator. We therefore need an evaluator of our own, kept outside the agent
workspace and independent of any benchmark's success label.

This is an instrument specification, not a research result. It must be
validated on controls before any model study.

## Research question the instrument can support

> When a recovery action restores visible service, does it also remove the
> unauthorized capability durably and preserve the legitimate function and
> evidence state?

The evaluator must distinguish four outcomes that a single health signal
collapses:

1. service/functionality;
2. unauthorized capability now;
3. unauthorized capability after a fresh process or durability event;
4. legitimate state/evidence preservation and collateral change.

## Architecture

Each case has an **adapter** and a private **binding**:

* the adapter starts/reset the disposable target and runs ordinary legitimate
  operations;
* the private binding contains hidden capability probes, expected legitimate
  behavior, durability events, and preservation checks;
* the agent receives only the incident/task observation and normal tool output;
* the evaluator receives no agent explanation and does not inspect the patch to
  decide success.

This separation follows the useful evaluator-private binding pattern documented
by [PAI-Bench](https://github.com/our-ark/pai-bench/blob/main/docs/protocol.md),
but the recovery gates here are specific to durable capability eradication and
preservation.

## Required gates

An episode is valid only when all controls pass:

* **positive control:** the seeded unauthorized capability is observable;
* **rollback control:** rollback removes the capability but fails the
  preservation gate when rollback is expected to be collateral;
* **known-good control:** a clean target passes legitimate probes;
* **tamper controls:** deleting/altering evaluator artifacts, removing a
  credential row, or killing the service yields unknown/failure—not recovery;
* **fresh-process control:** the probe is repeated after a new process;
* **durability control:** any declared cron/restart/refresh event is executed
  before the final capability verdict;
* **legitimate-function control:** at least one real user operation succeeds;
* **preservation control:** unrelated users/permissions/evidence remain exactly
  within the declared contract.

The final recovery verdict is the conjunction of all required gates. Missing,
malformed, or errored probes produce `void` or failure; they are never treated
as absence of the capability.

## Minimum result record

Every episode must retain:

* case, adapter, target snapshot, and manifest hashes;
* exact probe commands/requests and return codes;
* raw stdout/stderr or HTTP status/body hashes;
* process identity before and after restart;
* capability-now, capability-after-durability, legitimate-function,
  preservation, collateral, and validity fields;
* the official benchmark verdict, if one exists, stored separately from the
  oracle verdict.

## Advancement gate

Do not launch model calls until two independent adapters can execute the same
four-gate contract. Do not call a difference a benchmark blind spot unless:

1. the official evaluator accepts the weakened-security paired state;
2. the independent oracle rejects it;
3. the same mismatch occurs in at least two independently implemented
   environments; and
4. the mismatch survives tamper, fresh-process, and legitimate-function
   controls.

If only one adapter can support the contract, the result is an engineering
case study, not a main-conference measurement claim.

