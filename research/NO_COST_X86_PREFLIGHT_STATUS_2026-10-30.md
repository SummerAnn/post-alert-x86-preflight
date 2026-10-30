# No-cost x86 substrate status (2026-10-30)

This note records existing public GitHub Actions runs only. No workflow was dispatched by this check, no model/provider key was used, and no paid agent calls were made.

Repository: [SummerAnn/post-alert-x86-preflight](https://github.com/SummerAnn/post-alert-x86-preflight)

## Verified runs

- [Native x86 runtime preflight, run 40987428632](https://github.com/SummerAnn/post-alert-x86-preflight/actions/runs/40987428632): success. The hosted runner reported `x86_64`; Docker reported `arch=x86_64`; the pinned Kind cluster reached Ready with an `amd64` node; the exact AIOpsLab and SREGym commits were fetched; checked application images supported `linux/amd64`; the disposable cluster was deleted.
- [AIOpsLab credential-presence control, run 40996493991](https://github.com/SummerAnn/post-alert-x86-preflight/actions/runs/40996493991): success, explicitly labelled “no model.”
- [AIOpsLab TLS durability audit, run 40997031001](https://github.com/SummerAnn/post-alert-x86-preflight/actions/runs/40997031001): success, explicitly labelled “no model.”

The job logs provide the following independent checks:

- Credential control: official evaluator `success=True`; MongoDB authenticated the expected admin user with `readWrite` on `geo-db` and `userAdminAnyDatabase`; the frontend remained `Running`; the disposable Kind cluster was deleted.
- TLS durability audit: official evaluator `success=True`; plaintext MongoDB ping returned `1` both before and after replacing the MongoDB pod; the log marked `DURABILITY_CHECK=PASS`; the disposable Kind cluster was deleted.

## Interpretation

This removes the local ARM-only machine as a blocker for the *no-model* controls and provides a candidate x86 execution substrate. It does **not** establish that the frozen 24-cell agent study has run, and it does not make provider API calls free. The next safe action is another no-model control/preflight on this substrate; the agent pilot remains deliberately unlaunched until its API cost is separately approved.
