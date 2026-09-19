from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

DEFAULT_STATE_PATH = Path(".state/last_run.json")


def load_last_run(path: Path = DEFAULT_STATE_PATH) -> datetime | None:
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return datetime.fromisoformat(data["last_run"])


def save_last_run(when: datetime, path: Path = DEFAULT_STATE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"last_run": when.isoformat()}), encoding="utf-8")
