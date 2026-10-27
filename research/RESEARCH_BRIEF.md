# Research brief — initial, unfrozen

## Area

Post-alert recovery of systems modified by AI agents.

## What is not yet claimed

We do not currently claim that agents fail at recovery, verification,
discovering tools, preserving state, or handling external persistence. Those
were prior candidate claims, and the old repository contains both nulls and
confounded observations.

## Candidate question families

1. **Evidence boundary:** what information is necessary for safe recovery when
   the alert is incomplete or misleading?
2. **Recovery boundary:** when does an agent repair the harmful state while
   preserving legitimate subsequent changes?
3. **Closure boundary:** what independently verifiable evidence is required
   before an agent should resume operation?
4. **Multi-agent handoff:** how does recovery change when the agent that made
   the change is not the agent that receives the alert?

These are candidates, not selected research questions.

## First gate

Before implementation or model calls:

- map the closest published benchmarks and systems;
- identify one concrete unexplained phenomenon;
- verify that it is not merely a scorer or interface artifact;
- define a zero-cost feasibility test and a hard stop rule.

## Repository rule

Do not import old results into this project as support. They may motivate
questions, but each result must be independently re-established under a new,
frozen protocol.
