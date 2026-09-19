from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from inbox_agent.mail.gmail import GmailMailProvider


class _FakeRequest:
    def __init__(self, response: dict[str, Any]) -> None:
        self._response = response

    def execute(self) -> dict[str, Any]:
        return self._response


class _FakeMessages:
    def __init__(self, list_response: dict[str, Any], get_responses: dict[str, Any]) -> None:
        self._list_response = list_response
        self._get_responses = get_responses

    def list(self, userId: str, q: str, pageToken: str | None = None) -> _FakeRequest:
        return _FakeRequest(self._list_response)

    def get(self, userId: str, id: str, format: str, metadataHeaders: list[str]) -> _FakeRequest:
        return _FakeRequest(self._get_responses[id])


class _FakeUsers:
    def __init__(self, messages: _FakeMessages) -> None:
        self._messages = messages

    def messages(self) -> _FakeMessages:
        return self._messages


class _FakeService:
    def __init__(self, messages: _FakeMessages) -> None:
        self._users = _FakeUsers(messages)

    def users(self) -> _FakeUsers:
        return self._users


def _raw_message(sender: str, subject: str, snippet: str, internal_date_ms: int) -> dict[str, Any]:
    return {
        "internalDate": str(internal_date_ms),
        "snippet": snippet,
        "payload": {
            "headers": [
                {"name": "From", "value": sender},
                {"name": "Subject", "value": subject},
            ]
        },
    }


def test_fetch_new_messages_parses_headers_and_filters_by_exact_time() -> None:
    since = datetime(2026, 9, 19, 6, 0, tzinfo=timezone.utc)
    fresh_ms = int(datetime(2026, 9, 19, 7, 0, tzinfo=timezone.utc).timestamp() * 1000)
    stale_ms = int(datetime(2026, 9, 19, 5, 0, tzinfo=timezone.utc).timestamp() * 1000)

    fake_messages = _FakeMessages(
        list_response={"messages": [{"id": "1"}, {"id": "2"}]},
        get_responses={
            "1": _raw_message("szef@firma.pl", "Pilne", "Treść 1", fresh_ms),
            # Symuluje niedokładność filtra "after:" (dokładność do dnia) —
            # ta wiadomość jest zwrócona przez list(), ale jest starsza niż `since`.
            "2": _raw_message("stary@example.com", "Stare", "Treść 2", stale_ms),
        },
    )
    provider = GmailMailProvider(service=_FakeService(fake_messages))

    messages = provider.fetch_new_messages(since)

    assert len(messages) == 1
    assert messages[0].id == "1"
    assert messages[0].sender == "szef@firma.pl"
    assert messages[0].subject == "Pilne"
    assert messages[0].snippet == "Treść 1"
