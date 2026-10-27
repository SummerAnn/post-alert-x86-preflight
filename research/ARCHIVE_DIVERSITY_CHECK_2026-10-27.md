# Archive diversity check

The first downloaded ControlArena batch contained 24 evaluation files, but only two application/mechanism families:

* `incident-reporter / triggered-exfil / attack` (12 runs);
* `expense-tracker / triggered-exfil / attack` (12 runs).

The run IDs represent different agent trajectories and seeds, not different applications or attack mechanisms. The final-stage prompts and archive structure show the same two injected behaviors: environment-key leakage in incident reports and an API-key authorization header on expense export.

An additional public `agentic_auditor_logs` archive was then inspected. It contains a third application family: a monitoring/telemetry repository whose compromised state exfiltrates authentication context. This is a genuinely different active path and was added to the zero-model replay and repair pilot. The remaining runs in the first batch can support replication across trajectories, but they cannot support a claim that the observed tradeoff generalizes beyond these three mechanisms.

## Consequence

Do not spend more model calls on the remaining same-family runs yet. The next valid expansion requires a separately sourced artifact with a fourth persistence/capability mechanism (for example a scheduled task, durable credential, or database authorization state), and the same external evaluator must be adapted before looking at outcomes. If such an artifact cannot be obtained cheaply and reproducibly, the honest endpoint is a three-artifact feasibility result rather than a benchmark paper.

