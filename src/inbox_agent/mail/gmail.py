from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from inbox_agent.mail.base import MailProvider
from inbox_agent.models import EmailMessage

# Uprawnienie tylko do odczytu — agent nigdy nie modyfikuje ani nie wysyła poczty.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailMailProvider(MailProvider):
    """Dostawca Gmail API (tylko odczyt, OAuth2).

    Wymaga pliku danych klienta OAuth pobranego z Google Cloud Console
    (patrz README). Przy pierwszym uruchomieniu otwiera przeglądarkę do
    jednorazowej autoryzacji; token odświeżania jest potem cache'owany
    w `token_path` i używany automatycznie przy kolejnych uruchomieniach.
    """

    def __init__(
        self,
        client_secrets_path: str | None = None,
        token_path: str = ".state/gmail_token.json",
        query: str = "in:inbox -in:chats",
        service: Any | None = None,
    ) -> None:
        self._client_secrets_path = (
            Path(client_secrets_path) if client_secrets_path else None
        )
        self._token_path = Path(token_path)
        self._query = query
        self._service = service

    def fetch_new_messages(self, since: datetime) -> list[EmailMessage]:
        service = self._service or build("gmail", "v1", credentials=self._get_credentials())
        query = f"{self._query} after:{int(since.timestamp())}".strip()

        message_ids: list[str] = []
        page_token = None
        while True:
            response = (
                service.users()
                .messages()
                .list(userId="me", q=query, pageToken=page_token)
                .execute()
            )
            message_ids.extend(m["id"] for m in response.get("messages", []))
            page_token = response.get("nextPageToken")
            if not page_token:
                break

        messages = []
        for message_id in message_ids:
            detail = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id=message_id,
                    format="metadata",
                    metadataHeaders=["From", "Subject"],
                )
                .execute()
            )
            received_at = datetime.fromtimestamp(
                int(detail["internalDate"]) / 1000, tz=timezone.utc
            )
            # Gmail search operator "after:" filtruje z dokładnością do dnia,
            # więc doprecyzowujemy filtr po dokładnym czasie wiadomości.
            if received_at < since:
                continue

            headers = {h["name"]: h["value"] for h in detail["payload"]["headers"]}
            messages.append(
                EmailMessage(
                    id=message_id,
                    sender=headers.get("From", "(nieznany nadawca)"),
                    subject=headers.get("Subject", "(brak tematu)"),
                    snippet=detail.get("snippet", ""),
                    received_at=received_at,
                )
            )
        return messages

    def _get_credentials(self) -> Credentials:
        creds: Credentials | None = None
        if self._token_path.exists():
            creds = Credentials.from_authorized_user_file(str(self._token_path), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self._client_secrets_path or not self._client_secrets_path.exists():
                    raise FileNotFoundError(
                        "Nie znaleziono pliku danych klienta OAuth: "
                        f"{self._client_secrets_path}. Pobierz go z Google Cloud "
                        "Console (patrz README) i wskaż ścieżkę w "
                        "GMAIL_CLIENT_SECRETS_PATH."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self._client_secrets_path), SCOPES
                )
                creds = flow.run_local_server(port=0)

            self._token_path.parent.mkdir(parents=True, exist_ok=True)
            self._token_path.write_text(creds.to_json(), encoding="utf-8")

        return creds
