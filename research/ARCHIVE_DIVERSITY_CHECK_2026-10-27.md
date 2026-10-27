# Archive diversity check

The downloaded ControlArena archive contains 24 evaluation files, but only two application/mechanism families:

* `incident-reporter / triggered-exfil / attack` (12 runs);
* `expense-tracker / triggered-exfil / attack` (12 runs).

The run IDs represent different agent trajectories and seeds, not different applications or attack mechanisms. The final-stage prompts and archive structure show the same two injected behaviors: environment-key leakage in incident reports and an API-key authorization header on expense export.

Therefore the two-artifact recovery pilot is the maximum independent breadth available from this archive without constructing a new environment. The remaining runs can support replication across trajectories, but they cannot support a claim that the observed security–availability tradeoff generalizes across mechanisms.

## Consequence

Do not spend more model calls on the remaining same-family runs yet. The next valid expansion requires a separately sourced artifact with a different persistence/capability mechanism (for example a scheduled task, durable credential, or database authorization state), and the same external evaluator must be adapted before looking at outcomes. If such an artifact cannot be obtained cheaply and reproducibly, the honest endpoint is a two-artifact feasibility result rather than a benchmark paper.

