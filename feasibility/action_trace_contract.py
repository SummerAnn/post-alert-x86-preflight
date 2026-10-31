"""Fail-closed raw action trace records for the cross-system pilot.

This module does not execute actions or contact a provider.  It only defines the
minimum record that a later driver must emit for every model turn, preserving
the exact model text and the native parser result.  Missing/ambiguous actions
are voids, never silently dropped or converted to success.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ActionTurn:
    turn_index: int
    raw_response: str
    parsed_action: str | None
    parse_status: str


def record_turn(turn_index: int, raw_response: str, parsed_action: str | None) -> ActionTurn:
    """Create one immutable turn record with fail-closed parse semantics."""
    if not isinstance(turn_index, int) or turn_index < 0:
        raise ValueError("turn_index must be a non-negative integer")
    if not isinstance(raw_response, str):
        raise TypeError("raw_response must be text")
    if parsed_action is None:
        status = "void_missing_or_ambiguous_action"
    elif not isinstance(parsed_action, str) or not parsed_action.strip():
        raise ValueError("parsed_action must be non-empty text or None")
    else:
        status = "parsed"
    return ActionTurn(turn_index, raw_response, parsed_action, status)


def serialize_turn(turn: ActionTurn) -> dict[str, Any]:
    """Return a JSON-safe record without truncating the raw response."""
    return {
        "turn_index": turn.turn_index,
        "raw_response": turn.raw_response,
        "parsed_action": turn.parsed_action,
        "parse_status": turn.parse_status,
    }
