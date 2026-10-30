# Draft amendment: baseline semantics for verifier-feedback study

**Status:** design draft only; not frozen; no model calls.

## Problem being repaired

The current preregistration requires a clean pre-fault `known_good` state to
pass the post-incident security invariant. Both selected mechanisms install
the security control as part of fault injection, so their clean baselines fail
that predicate by construction.

## Minimal proposed repair: incident-relative controls

For each mechanism, use three mechanically distinct states:

1. **incident-known-good:** apply the security control, but do not trigger the
   availability failure; verify availability, security, function, and fresh
   process/pod durability;
2. **secure repair:** inject the full incident, then retain the security
   control and repair the workload/dependency;
3. **rollback:** inject the full incident, then apply the released
   availability-first recovery; verify availability but security failure.

The agent episodes still begin only after full fault injection. The first row
is a controller sanity control, not an agent state. The amendment must record
the exact ordering and state hashes so the control is not confused with the
clean pre-fault baseline.

## Why this is not yet accepted

This changes the frozen control semantics and requires live no-model truth
tables on native-compatible artifacts. It must also verify that the secure
repair is feasible without using hidden oracle information. Until those checks
are complete, the existing 24-cell pilot remains blocked.

## Replacement path

If reviewers reject incident-relative controls, the alternative is a released
mechanism with a security-preserving clean baseline. SREGym's MongoDB
`revoke_auth` and `storage_user_unregistered` tasks are static candidates
because they start with an authenticated database user/role, but their
availability/security paired controls are not yet implemented or validated.
