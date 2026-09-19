from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


class ConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class Config:
    anthropic_api_key: str
    mail_provider: str
    mock_inbox_path: str | None
    gmail_client_secrets_path: str | None
    gmail_token_path: str
    gmail_query: str


def load_config() -> Config:
    load_dotenv()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ConfigError(
            "Brak ANTHROPIC_API_KEY w środowisku. Ustaw go w pliku .env "
            "(patrz .env.example)."
        )

    return Config(
        anthropic_api_key=api_key,
        mail_provider=os.environ.get("MAIL_PROVIDER", "mock"),
        mock_inbox_path=os.environ.get("MOCK_INBOX_PATH"),
        gmail_client_secrets_path=os.environ.get("GMAIL_CLIENT_SECRETS_PATH"),
        gmail_token_path=os.environ.get("GMAIL_TOKEN_PATH", ".state/gmail_token.json"),
        gmail_query=os.environ.get("GMAIL_QUERY", "in:inbox -in:chats"),
    )
