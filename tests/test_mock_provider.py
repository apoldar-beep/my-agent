from __future__ import annotations

from datetime import datetime, timedelta, timezone

from inbox_agent.mail.mock import MockMailProvider


def test_returns_only_messages_newer_than_since() -> None:
    provider = MockMailProvider()
    now = datetime.now(timezone.utc)

    all_messages = provider.fetch_new_messages(now - timedelta(days=1))
    assert len(all_messages) == 3

    only_recent = provider.fetch_new_messages(now - timedelta(minutes=60))
    assert len(only_recent) == 1
    assert only_recent[0].sender == "szef@firma.pl"


def test_returns_nothing_when_since_is_in_the_future() -> None:
    provider = MockMailProvider()
    now = datetime.now(timezone.utc)

    assert provider.fetch_new_messages(now + timedelta(hours=1)) == []
