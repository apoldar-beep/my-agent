from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from inbox_agent.mail.base import MailProvider
from inbox_agent.models import EmailMessage

_SAMPLE_MESSAGES = [
    {
        "sender": "szef@firma.pl",
        "subject": "Pilne: raport na jutro rano",
        "snippet": "Potrzebuję wersji finalnej przed 9:00.",
        "offset_minutes": 30,
    },
    {
        "sender": "newsletter@serwis.pl",
        "subject": "Twój tygodniowy przegląd",
        "snippet": "Podsumowanie aktywności w tym tygodniu.",
        "offset_minutes": 120,
    },
    {
        "sender": "klient@example.com",
        "subject": "Pytanie o termin spotkania",
        "snippet": "Czy pasuje Ci czwartek 14:00?",
        "offset_minutes": 200,
    },
]


class MockMailProvider(MailProvider):
    """Dostawca testowy — generuje przykładowe wiadomości albo wczytuje je
    z pliku JSON (`fixture_path`). Zastąp konkretną implementacją
    (np. Gmail API, IMAP) po wybraniu prawdziwego dostawcy poczty."""

    def __init__(self, fixture_path: str | None = None) -> None:
        self._fixture_path = Path(fixture_path) if fixture_path else None

    def fetch_new_messages(self, since: datetime) -> list[EmailMessage]:
        if self._fixture_path:
            return self._load_fixture()

        now = datetime.now(timezone.utc)
        messages = []
        for i, m in enumerate(_SAMPLE_MESSAGES):
            received_at = now - timedelta(minutes=m["offset_minutes"])
            if received_at >= since:
                messages.append(
                    EmailMessage(
                        id=str(i),
                        sender=m["sender"],
                        subject=m["subject"],
                        snippet=m["snippet"],
                        received_at=received_at,
                    )
                )
        return messages

    def _load_fixture(self) -> list[EmailMessage]:
        assert self._fixture_path is not None
        data = json.loads(self._fixture_path.read_text(encoding="utf-8"))
        return [
            EmailMessage(
                id=item["id"],
                sender=item["sender"],
                subject=item["subject"],
                snippet=item.get("snippet", ""),
                received_at=datetime.fromisoformat(item["received_at"]),
            )
            for item in data
        ]
