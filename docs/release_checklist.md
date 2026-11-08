# Nettlewood Release Checklist

Pre-flight checklist for the 2.4.x release series. Every entry references
a source location that still needs follow-up work before the tag is cut.

## Open Items

- [ ] **src/nettlewood/engine/runner.py:61** - Add timeout handling for pipeline stages
- [ ] **src/nettlewood/engine/runner.py:98** - Document stage retry semantics
- [ ] **src/nettlewood/storage/wal.py:36** - Cover checkpoint truncation edge case

## Sign-off

- [ ] Review the checklist with the release manager
- [ ] Confirm the changelog is current
