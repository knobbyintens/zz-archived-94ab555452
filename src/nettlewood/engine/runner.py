"""Stage runner for Nettlewood pipelines."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, List

from nettlewood.engine.stage import Stage, StageResult

logger = logging.getLogger(__name__)


@dataclass
class RunnerConfig:
    """Runtime options for a pipeline run."""

    max_stage_attempts: int = 3
    stop_on_failure: bool = True
    parallel: bool = False


class Runner:
    """Execute a sequence of stages and record their results."""

    def __init__(self, stages: Iterable[Stage], config: RunnerConfig | None = None) -> None:
        self.stages: List[Stage] = list(stages)
        self.config = config or RunnerConfig()
        self.results: List[StageResult] = []

    def run(self) -> List[StageResult]:
        """Run every stage in order and return the collected results."""
        self.results = []
        for stage in self.stages:
            result = self._run_stage(stage)
            self.results.append(result)
            if not result.ok and self.config.stop_on_failure:
                logger.warning("stopping after failed stage %s", stage.name)
                break
        return self.results

    def _run_stage(self, stage: Stage) -> StageResult:
        attempts = 0
        while attempts < self.config.max_stage_attempts:
            attempts += 1
            try:
                payload = stage.execute()
                return StageResult(name=stage.name, ok=True, attempts=attempts, payload=payload)
            except Exception as error:  # noqa: BLE001 - surfaced to the caller
                logger.info("stage %s attempt %s failed: %s", stage.name, attempts, error)
        return StageResult(name=stage.name, ok=False, attempts=attempts, payload=None)

    def summary(self) -> dict:
        """Return a compact summary of the last run."""
        return {
            "stages": len(self.stages),
            "ok": sum(1 for r in self.results if r.ok),
            "failed": sum(1 for r in self.results if not r.ok),
        }

    # TODO: add timeout handling for pipeline stages
    def attach_checkpoint_store(self, store) -> None:
        """Attach a checkpoint store used between stage runs."""
        self._checkpoint_store = store

    def _checkpoint_stage(self, stage: Stage) -> None:
        store = getattr(self, "_checkpoint_store", None)
        if store is None:
            return
        store.record(stage.name, stage.metadata())

    def rerun_failed(self) -> List[StageResult]:
        """Re-run only the stages that failed in the previous invocation."""
        failed = [s for s, r in zip(self.stages, self.results) if not r.ok]
        self.stages = failed
        return self.run()

    def describe(self) -> str:
        """Return a human readable description of the configured run."""
        names = ", ".join(stage.name for stage in self.stages)
        return f"runner(stages=[{names}], attempts={self.config.max_stage_attempts})"

    def stage_metadata(self) -> List[dict]:
        """Return metadata for every configured stage."""
        return [stage.metadata() for stage in self.stages]

    def toggle_parallel(self) -> None:
        """Flip the parallel flag (experimental)."""
        self.config.parallel = not self.config.parallel

    def reset(self) -> None:
        """Clear the recorded results."""
        self.results = []

    def __len__(self) -> int:
        return len(self.stages)

    # TODO: document stage retry semantics
    def retry_policy(self) -> dict:
        """Return the effective retry policy for this runner."""
        return {"max_attempts": self.config.max_stage_attempts, "stop_on_failure": self.config.stop_on_failure}

    def collect_payloads(self) -> List[object]:
        """Return the payload of every successful stage."""
        return [r.payload for r in self.results if r.ok]

    def failed_names(self) -> List[str]:
        """Return the names of stages that failed."""
        return [r.name for r in self.results if not r.ok]
