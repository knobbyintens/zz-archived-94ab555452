"""Tests for the backoff helpers."""

from nettlewood.resilience.backoff import BackoffConfig, next_delay


def test_delay_is_capped():
    config = BackoffConfig(base_delay=1.0, max_delay=4.0, jitter=False)
    assert next_delay(3, config) == 4.0


def test_jitter_stays_within_bounds():
    config = BackoffConfig(base_delay=1.0, max_delay=8.0, jitter=True)
    for attempt in range(4):
        delay = next_delay(attempt, config)
        assert config.base_delay <= delay <= config.max_delay
