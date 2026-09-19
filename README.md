# Inbox Agent — poranne podsumowanie skrzynki odbiorczej

Agent, który czyta nowe wiadomości e-mail i generuje jednostronicowe
podsumowanie najważniejszych rzeczy. Zasady działania (format wyjścia,
zakres, bezpieczeństwo) opisuje `CLAUDE.md`.

## Status

To jest szkielet projektu. Pobieranie poczty jest na razie realizowane
przez `MockMailProvider` (dane testowe) — prawdziwy dostawca (Gmail API,
IMAP, …) nie został jeszcze wybrany ani zaimplementowany.

## Instalacja

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"
    cp .env.example .env   # i uzupełnij ANTHROPIC_API_KEY

## Uruchomienie

    python -m inbox_agent.main

Podsumowanie trafia do `summaries/<data>.md`. Czas ostatniego
uruchomienia jest zapisywany w `.state/last_run.json`, dzięki czemu
kolejne uruchomienie pobiera tylko wiadomości nowsze niż poprzednie.

## Testy

    pytest

## Struktura

    src/inbox_agent/
      config.py      — wczytywanie konfiguracji z env (nic na sztywno)
      models.py       — model EmailMessage
      mail/base.py    — interfejs MailProvider (zaimplementuj dla realnego dostawcy)
      mail/mock.py     — testowy dostawca danych
      summarizer.py    — budowa promptu i wywołanie Anthropic API
      output.py        — zapis podsumowania do pliku Markdown
      state.py         — śledzenie czasu ostatniego uruchomienia
      main.py          — orkiestracja całego przebiegu

## Dodanie prawdziwego dostawcy poczty

1. Zaimplementuj klasę dziedziczącą po `inbox_agent.mail.base.MailProvider`
   (metoda `fetch_new_messages(since)`).
2. Podłącz ją w `inbox_agent/main.py::get_mail_provider`.
3. Dodaj wymagane zmienne konfiguracyjne do `.env.example` i `config.py`.
