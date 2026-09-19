from __future__ import annotations

from datetime import date
from pathlib import Path

DEFAULT_SUMMARIES_DIR = Path("summaries")


def write_summary(text: str, today: date, base_dir: Path = DEFAULT_SUMMARIES_DIR) -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)
    path = base_dir / f"{today.isoformat()}.md"
    path.write_text(text, encoding="utf-8")
    return path
