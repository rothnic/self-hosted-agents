from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ActorStep:
    actor: str
    text: str


@dataclass(frozen=True)
class Observation:
    name: str
    ok: bool
    evidence: dict[str, Any]


class BehaviorDriver(Protocol):
    name: str

    def start(self) -> None:
        """Prepare the implementation under test."""

    def act(self, step: ActorStep) -> None:
        """Perform an actor-level action from the scenario."""

    def observe(self, assertion: str) -> Observation:
        """Return user-facing or operational evidence for an assertion."""

    def stop(self) -> None:
        """Clean up resources."""
