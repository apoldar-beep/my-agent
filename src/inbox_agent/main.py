from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from inbox_agent.config import Config, ConfigError, load_config
from inbox_agent.mail.base import MailProvider
from inbox_agent.mail.gmail import GmailMailProvider
from inbox_agent.mail.mock import MockMailProvider
from inbox_agent.output import write_summary
from inbox_agent.state import load_last_run, save_last_run
from inbox_agent.summarizer import build_summary

FIRST_RUN_WINDOW = timedelta(hours=24)


def get_mail_provider(config: Config) -> MailProvider:
    if config.mail_provider == "mock":
        return MockMailProvider(config.mock_inbox_path)
    if config.mail_provider == "gmail":
        if not config.gmail_client_secrets_path:
            raise ConfigError(
                "MAIL_PROVIDER=gmail wymaga GMAIL_CLIENT_SECRETS_PATH w .env "
                "(ścieżka do pliku danych klienta OAuth z Google Cloud Console; "
                "patrz README)."
            )
        return GmailMailProvider(
            client_secrets_path=config.gmail_client_secrets_path,
            token_path=config.gmail_token_path,
            query=config.gmail_query,
        )
    raise NotImplementedError(
        f"Dostawca poczty '{config.mail_provider}' nie jest jeszcze zaimplementowany. "
        "Zaimplementuj inbox_agent.mail.base.MailProvider dla wybranego dostawcy "
        "i podłącz go tutaj."
    )


def run() -> None:
    config = load_config()
    provider = get_mail_provider(config)

    now = datetime.now(timezone.utc)
    since = load_last_run() or (now - FIRST_RUN_WINDOW)

    messages = provider.fetch_new_messages(since)
    summary = build_summary(messages, date.today(), config.anthropic_api_key)
    path = write_summary(summary, date.today())
    save_last_run(now)

    print(f"Zapisano podsumowanie: {path}")


if __name__ == "__main__":
    run()
