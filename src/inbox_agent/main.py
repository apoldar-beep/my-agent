from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from inbox_agent.config import load_config
from inbox_agent.mail.base import MailProvider
from inbox_agent.mail.mock import MockMailProvider
from inbox_agent.output import write_summary
from inbox_agent.state import load_last_run, save_last_run
from inbox_agent.summarizer import build_summary

FIRST_RUN_WINDOW = timedelta(hours=24)


def get_mail_provider(provider_name: str, mock_inbox_path: str | None) -> MailProvider:
    if provider_name == "mock":
        return MockMailProvider(mock_inbox_path)
    raise NotImplementedError(
        f"Dostawca poczty '{provider_name}' nie jest jeszcze zaimplementowany. "
        "Zaimplementuj inbox_agent.mail.base.MailProvider dla wybranego dostawcy "
        "i podłącz go tutaj."
    )


def run() -> None:
    config = load_config()
    provider = get_mail_provider(config.mail_provider, config.mock_inbox_path)

    now = datetime.now(timezone.utc)
    since = load_last_run() or (now - FIRST_RUN_WINDOW)

    messages = provider.fetch_new_messages(since)
    summary = build_summary(messages, date.today(), config.anthropic_api_key)
    path = write_summary(summary, date.today())
    save_last_run(now)

    print(f"Zapisano podsumowanie: {path}")


if __name__ == "__main__":
    run()
