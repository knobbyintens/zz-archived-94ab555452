# Nettlewood 2.4 Upgrade Notes

The 2.4 series focuses on resumable and observable pipeline stages.

1. Checkpoints are now written through the write-ahead log by default.
2. Retry behaviour is configurable per stage through `BackoffConfig`.
3. Stage timeouts will become mandatory for long-running pipelines.

## Compatibility

Existing pipelines keep working, but the default retry budget changed from
three attempts to five. Review your stage implementations before upgrading.

## Action required

Re-run your pipeline smoke tests with the new defaults and confirm that each
stage can be retried safely.
