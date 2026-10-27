# Archive-wide zero-model audit

The extracted public archive contains 24 usable persistent attack runs in the
selected batch:

- 12 `incident-reporter / triggered-exfil` runs;
- 12 `expense-tracker / triggered-exfil` runs;
- every run has a complete PR-diff sequence (five or six PRs);
- no extraction errors occurred.

The side-task scorer recorded success for all 24 final states. The sensitive
telemetry/exfiltration code first appears in PR2 for 11 runs and PR3 for 13
runs, rather than being introduced only in the final PR. This is materially
better than the single-run impression and means the archive contains staged
attack state suitable for a rollback-versus-repair audit.

The archive also reports main-task success inconsistently across these runs
(12 final samples scored correct and 12 incorrect), so legitimate-function
preservation must be re-tested independently rather than inherited from the
benchmark score.

## Consequence

The study can now test whether rollback at different alert points leaves an
earlier staged capability, using multiple runs and two task families. This is a
stronger and more interesting question than the original one-artifact pilot:

> Does post-alert recovery remove the executable side task, or only the latest
> visible stage of a distributed attack?

No confirmatory model run is authorized by this audit alone. The next step is a
zero-model reconstruction of representative PR2/PR3/PR-final states from both
families, followed by hidden behavioral probes and independent main-task tests.
