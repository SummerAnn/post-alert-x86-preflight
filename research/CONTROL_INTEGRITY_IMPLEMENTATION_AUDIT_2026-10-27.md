# Control-integrity implementation audit — 2026-10-27

## Result

The existing repository provides strong **independent capability probing** and
fail-closed scoring, but it does not provide the causal control-integrity setup
needed for the new hypothesis.

Existing recovery harnesses can:

- keep probes out of the agent-visible environment;
- test API-enforced capability after durability events;
- separate legitimate functionality from capability removal;
- record raw commands and probe results.

They cannot currently show that an agent changed the effective behavior of a
safety control while leaving the monitor-visible configuration or trace
apparently normal. The controls are either ordinary application state or
out-of-band probes; there is no independent monitor whose observation path can
be selectively weakened.

## Consequence

The control-integrity hypothesis cannot be validated by relabeling the old H1
or path-closure experiments. Doing so would repeat the same measurement error:
capability recovery is not the same as control-integrity failure.

## What a real implementation would require

At least two real controls with three separated surfaces:

1. effective behavior (the control actually blocks or permits an action);
2. monitor-visible configuration/trace;
3. independent out-of-band behavioral probe.

The agent must be able to influence one surface without trivially changing all
three. The current repository does not yet contain such a substrate.

## Gate decision

No model pilot is justified yet. The next work, if continued, is substrate
discovery from an existing open-source containment or agent-runtime system—not
another experiment in the current recovery harness.
