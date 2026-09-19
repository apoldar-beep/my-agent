from __future__ import annotations

from datetime import date

from inbox_agent.summarizer import build_summary


def test_empty_inbox_produces_placeholder_without_calling_api() -> None:
    summary = build_summary([], date(2026, 9, 19), api_key="unused")

    assert "2026-09-19" in summary
    assert "Brak nowych wiadomości" in summary
