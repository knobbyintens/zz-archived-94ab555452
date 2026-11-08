"""Write-ahead log storage for checkpoints."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Iterable, List


class WriteAheadLog:
    """Append-only record of checkpoint mutations."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "checkpoints.wal"

    def append(self, record: dict) -> None:
        """Append one serialized record to the log."""
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    def replay(self) -> List[dict]:
        """Return every record currently stored in the log."""
        if not self.path.exists():
            return []
        records = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    # TODO: cover checkpoint truncation edge case
    def truncate(self, keep: int) -> None:
        """Keep only the newest ``keep`` records."""
        records = self.replay()[-keep:]
        tmp = self.path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record, sort_keys=True) + "\n")
        os.replace(tmp, self.path)
