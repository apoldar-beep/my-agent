from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from inbox_agent.models import EmailMessage


class MailProvider(ABC):
    """Interfejs dostawcy poczty. Zaimplementuj tę klasę dla wybranego
    dostawcy (np. Gmail API, IMAP) i podłącz w main.py::get_mail_provider."""

    @abstractmethod
    def fetch_new_messages(self, since: datetime) -> list[EmailMessage]:
        """Zwraca wiadomości otrzymane po `since` (kolejność dowolna)."""
