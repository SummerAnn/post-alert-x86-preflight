# Erratum D: checkpoint-budget handling — 2026-10-30

The first cell after the corrected PSA gate requested a third checkpoint. The
controller correctly rejected it, but the exploratory runner crashed instead
of returning a generic budget-exhausted tool result. The cell and the partial
batch are excluded. The runner now converts only this expected budget boundary
into `{"checkpoint":"budget_exhausted"}` and keeps the episode alive until
the fixed turn limit or an explicit finish action. No oracle output is exposed
and the two-checkpoint cap is unchanged.

