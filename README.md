# Nettlewood

Nettlewood is a lightweight, checkpointed task orchestration library for
reproducible Python data pipelines. It focuses on resumable stages, explicit
checkpoints and predictable retry behaviour.

## Repository layout

- `src/nettlewood/engine/` - stage scheduling and execution
- `src/nettlewood/resilience/` - retry and backoff helpers
- `src/nettlewood/storage/` - checkpoint and write-ahead-log handling
- `docs/` - release checklists and upgrade notes

## Development

```
pip install -e .
pytest -q
```

Release follow-up work is tracked in `docs/release_checklist.md`. Entries point
at the exact source line that still needs attention. The list is reviewed before
each release tag is cut.
