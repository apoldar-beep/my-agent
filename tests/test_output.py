from __future__ import annotations

from datetime import date
from pathlib import Path

from inbox_agent.output import write_summary


def test_writes_markdown_file_named_by_date(tmp_path: Path) -> None:
    path = write_summary("treść podsumowania", date(2026, 9, 19), base_dir=tmp_path)

    assert path == tmp_path / "2026-09-19.md"
    assert path.read_text(encoding="utf-8") == "treść podsumowania"
