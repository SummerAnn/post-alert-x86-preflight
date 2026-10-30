"""Controller contract for nonterminal verifier feedback.

The released benchmark runners currently evaluate only after submission.  This
module defines the smallest wrapper needed for the proposed intervention while
keeping the final released evaluator separate.  It deliberately accepts
callables rather than importing either benchmark, so tests can prove the
feedback and nontermination invariants without a cluster or model call.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from verifier_feedback import FeedbackCondition, VerifierFeedback, build_feedback


class CheckpointProtocolError(RuntimeError):
    """Raised when the wrapper cannot preserve the frozen episode contract."""


@dataclass(frozen=True)
class CheckpointAudit:
    """Researcher-visible record; never serialized into the agent message."""

    checkpoint_index: int
    official_availability: bool
    hidden_security_invariant: bool
    condition: FeedbackCondition
    episode_remained_open: bool


@dataclass(frozen=True)
class CheckpointResult:
    """The agent-visible feedback plus the hidden audit record."""

    feedback: VerifierFeedback
    audit: CheckpointAudit


class CheckpointController:
    """Run two read-only checks and return only preregistered feedback.

    ``official_availability_oracle`` must be the unchanged released health
    predicate bound by the live adapter. ``hidden_security_oracle`` is kept
    outside the agent process. ``final_evaluator`` is called only by
    :meth:`finalize`, after the agent terminates, and is never replaced by the
    checkpoint path.
    """

    def __init__(
        self,
        *,
        official_availability_oracle: Callable[[Any], bool],
        hidden_security_oracle: Callable[[Any], bool],
        final_evaluator: Callable[[Any], Mapping[str, Any]],
        max_checkpoints: int,
    ) -> None:
        if max_checkpoints < 1:
            raise ValueError("max_checkpoints must be positive")
        self._official = official_availability_oracle
        self._hidden = hidden_security_oracle
        self._final = final_evaluator
        self._max_checkpoints = max_checkpoints
        self._records: list[CheckpointAudit] = []

    @property
    def records(self) -> tuple[CheckpointAudit, ...]:
        """Return immutable researcher-visible checkpoint records."""
        return tuple(self._records)

    def checkpoint(
        self,
        state: Any,
        *,
        condition: FeedbackCondition,
        episode_open: bool,
    ) -> CheckpointResult:
        """Evaluate a nonterminal checkpoint and preserve episode liveness."""
        if not episode_open:
            raise CheckpointProtocolError("checkpoint requested after episode termination")
        if len(self._records) >= self._max_checkpoints:
            raise CheckpointProtocolError("checkpoint budget exhausted")

        # The two calls are intentionally made before rendering any agent
        # message.  Their raw outputs stay in controller scope.
        official = self._official(state)
        hidden = self._hidden(state)
        if not isinstance(official, bool) or not isinstance(hidden, bool):
            raise CheckpointProtocolError("oracle outputs must be boolean")

        feedback = build_feedback(
            condition=condition,
            availability=official,
            security_invariant=hidden,
        )
        audit = CheckpointAudit(
            checkpoint_index=len(self._records),
            official_availability=official,
            hidden_security_invariant=hidden,
            condition=condition,
            episode_remained_open=episode_open,
        )
        self._records.append(audit)
        return CheckpointResult(feedback=feedback, audit=audit)

    def finalize(self, state: Any) -> Mapping[str, Any]:
        """Call the released final evaluator exactly as supplied."""
        result = self._final(state)
        if not isinstance(result, Mapping):
            raise CheckpointProtocolError("final evaluator returned a non-mapping result")
        return result

