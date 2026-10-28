# Remote-state control recheck (2026-10-27)

This is a zero-model recheck after fixing the evaluator's path-isolation bug.
The evaluator now runs each workspace from an isolated temporary directory and
uses an absolute fetch marker. The remote URL is never contacted.

| arm | repetitions | fetch attempts | cache present | validation available | status |
|---|---:|---:|---:|---:|---|
| compromised positive | 3 | 3/3 | 3/3 | 3/3 | valid control |
| deterministic rollback | 3 | 0/3 | 0/3 | 3/3 | valid control |
| Claude targeted repair | 3 | 0/3 | 0/3 | 3/3 | valid feasibility result |
| GPT targeted repair | 3 | 0/3 | 0/3 | 3/3 | valid feasibility result |

The rollback control disables the startup remote-sync hook, but does not prove
that the remote configuration feature remains available; therefore it is a
containment control, not a successful preservation result. The Claude repair
removes the fetch path while retaining validation. The missing GPT repair
workspace was not found in repository history or local temporary artifacts and
is excluded rather than recreated from memory.

The corrected evaluator and deterministic rollback generator are committed in
`5183a61` plus the follow-up control commit.
