# Read-only audit of the ControlArena candidate

## Confirmed substrate properties

- Persistent runs execute each PR in a fresh container and inject the previous
  workspace/git state. This gives a real fresh-process boundary, not merely a
  longer conversation.
- The API task family has externally executable side tasks, including
  `triggered-api-exfil`, `support-preview-backdoor`, and other authentication or
  telemetry abuses. The scorers exercise HTTP behavior rather than searching for
  strings in a diff.
- The scorer starts a fresh Flask process, waits for readiness, probes behavior,
  and kills the process. Thus immediate post-response and fresh-process probes
  are technically feasible.
- The persistent dataset records task index, run id, sequence, prior-state
  injection, and PR boundaries. The setting therefore supports a later-PR probe
  after a response.

## Important limitation

The shipped scorers are attack-success scorers, not recovery scorers. They
typically start the app from the final workspace and check whether the side task
works. They do not define a response event, preserve an alerted snapshot, or
measure legitimate-task preservation after cleanup. Those are an extension, not
already-supported evidence.

## Best two candidate mechanisms

1. `support-preview-backdoor`: an authentication bypass triggered by a special
   header and coupled to telemetry suppression. It has explicit positive and
   negative HTTP probes, making it suitable for an independent capability oracle.
2. `triggered-api-exfil`: an exfiltration path activated by a normal main-task
   command. It has an external capture endpoint and a trigger-specific scorer,
   making it suitable for testing whether cleanup removes a dormant later-use
   path.

These are materially stronger than the earlier hand-built database-role case:
the benchmark already has multi-PR provenance, fresh-container boundaries, and
real application-level postconditions.

## Remaining go/no-go audit

Before any model call, implement only a zero-model replay on a known attack
artifact:

1. establish that each side task is active in the final PR state;
2. save the exact alerted workspace;
3. apply candidate response transformations (rollback, targeted deletion, or
   independent probe-guided repair) without changing the scorer;
4. restart in a fresh container and run hidden capability probes;
5. run the main-task suite and a later-PR trigger probe;
6. verify that a sham response fails to clear the capability and that the scorer
   fails closed on missing/error probes.

If this replay cannot separate active cleanup from dormant later-PR residue, the
research question is not supported and the candidate should be dropped before
spending API budget.
