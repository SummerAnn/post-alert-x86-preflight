# Erratum B: turn-budget correction for the SREGym exploratory pilot — 2026-10-30

The first four exploratory cells were completed but are classified
**incomplete**, not as outcomes: the eight-turn cap truncated every episode
before a terminal recovery. One cell localized the PSA fault and issued a
partial secure patch, but the service never reached the terminal evaluator;
the other cells were still inspecting state. The released SREGym mitigation
configuration allows 20 steps.

Before interpreting any feedback contrast, fresh episodes are therefore
rerun with a fixed 16-turn cap and the same two models, two conditions, tools,
checkpoint budget, initial prompt, hidden-oracle separation, and teardown
rules. The original eight-turn traces remain immutable in their original
directory and are reported as incomplete. The rerun remains exploratory and
is not pooled with the first attempt or treated as confirmatory evidence.

