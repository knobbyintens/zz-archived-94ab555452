"""Exponential backoff helpers for retryable Nettlewood stages."""

from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass
class BackoffConfig:
    """Configuration for capped exponential backoff."""

    base_delay: float = 0.5
    max_delay: float = 30.0
    multiplier: float = 2.0
    jitter: bool = True
    max_attempts: int = 5
    sleep: Callable[[float], None] = field(default=time.sleep, repr=False)


class RetryExceeded(RuntimeError):
    """Raised when the retry budget for a stage is exhausted."""


def next_delay(attempt: int, config: BackoffConfig) -> float:
    """Return the capped exponential delay for the given attempt."""
    raw = config.base_delay * (config.multiplier ** attempt)
    capped = min(raw, config.max_delay)
    if not config.jitter:
        return capped
    # Full jitter keeps thundering herds from lining up after an outage.
    return random.uniform(config.base_delay, capped)


def run_with_backoff(
    operation: Callable[[], object],
    config: Optional[BackoffConfig] = None,
) -> object:
    """Execute an operation with capped exponential backoff."""
    # TODO: document jitter cap behaviour for exponential backoff
    config = config or BackoffConfig()
    last_error: Optional[BaseException] = None
    for attempt in range(config.max_attempts):
        try:
            return operation()
        except BaseException as error:
            last_error = error
            if attempt == config.max_attempts - 1:
                break
            config.sleep(next_delay(attempt, config))
    raise RetryExceeded(f"operation failed after {config.max_attempts} attempts") from last_error
