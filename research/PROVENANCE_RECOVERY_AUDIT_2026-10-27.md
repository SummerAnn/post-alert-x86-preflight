# Compliance artifact provenance audit (2026-10-27)

## Result

The current repository contains the evaluator, repair prompts, pilot manifests,
and reconstruction notes, but no retained `validator.py`, `metrics.py`,
`validator_config.yaml`, `configs/`, or reconstructed compliance workspace.
The temporary workspace paths referenced by the pilot scripts are absent. No
model or evaluator result was changed by this audit.

## Recoverable provenance

The reconstruction notes identify the public source as commit `5922d8b` of the
Hugging Face dataset
`idacy/control-arena-persistent-state-eval-archive-2026-07-30`. Its dataset
card states that the archive is a local-workspace archive and that the larger
`logs/Josh3/` tree, including the relevant evaluation logs, is stored in a
separate companion archive rather than in this repository:

<https://huggingface.co/datasets/idacy/control-arena-persistent-state-eval-archive-2026-07-30/blob/main/README.md>

The archive documents the relevant `config-validator` paths and the expected
source history, but the source workspace itself is not a small local file that
can be safely reconstructed from this repository alone. Downloading the
multi-gigabyte source archive is therefore not part of this zero-cost gate.

## Consequence

The compliance-v2 difficulty design is not yet an executable artifact. Before
any new model call, one of the following must happen:

1. recover a specific archived run and its source files from the public archive,
   with hashes and an extraction manifest; or
2. close this candidate and use another independently available application.

Recreating missing application behavior by hand would violate the provenance
requirement and could manufacture the very difficulty we want to measure.

