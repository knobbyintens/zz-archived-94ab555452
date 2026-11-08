"""Stage primitives for Nettlewood pipelines."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict


@dataclass
class StageResult:
    """Outcome of a single stage execution."""

    name: str
    ok: bool
    attempts: int
    payload: Any = None


@dataclass
class Stage:
    """A unit of work in a Nettlewood pipeline."""

    name: str
    func: Callable[[], Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def execute(self) -> Any:
        """Run the stage function and return its payload."""
        return self.func()
