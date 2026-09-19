# Inbox Agent — poranne podsumowanie skrzynki odbiorczej

Agent, który czyta nowe wiadomości e-mail i generuje jednostronicowe
podsumowanie najważniejszych rzeczy. Zasady działania (format wyjścia,
zakres, bezpieczeństwo) opisuje `CLAUDE.md`.

## Status

Dostępne dostawce poczty: `mock` (dane testowe, domyślny) i `gmail`
(Gmail API, tylko odczyt). Inne dostawcy (IMAP, …) nie są jeszcze
zaimplementowani.

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
      mail/gmail.py    — dostawca Gmail API (OAuth2, tylko odczyt)
      summarizer.py    — budowa promptu i wywołanie Anthropic API
      output.py        — zapis podsumowania do pliku Markdown
      state.py         — śledzenie czasu ostatniego uruchomienia
      main.py          — orkiestracja całego przebiegu

## Konfiguracja Gmail API

1. W [Google Cloud Console](https://console.cloud.google.com/) utwórz
   projekt (lub użyj istniejącego) i włącz **Gmail API**
   (API i usługi → Biblioteka).
2. Skonfiguruj ekran zgody OAuth (typ „Zewnętrzny”, tryb testowy)
   i dodaj swój adres Gmail jako testera.
3. Utwórz dane logowania → **Identyfikator klienta OAuth** → typ
   aplikacji **Desktop app**. Pobierz plik JSON (np. `client_secret.json`).
4. W `.env` ustaw:

       MAIL_PROVIDER=gmail
       GMAIL_CLIENT_SECRETS_PATH=/ścieżka/do/client_secret.json

5. Uruchom `python -m inbox_agent.main` **lokalnie, na maszynie z
   przeglądarką** — przy pierwszym uruchomieniu otworzy się okno
   autoryzacji Google. Zakres to `gmail.readonly` (tylko odczyt —
   agent nigdy nie modyfikuje ani nie wysyła poczty). Token odświeżania
   zostanie zapisany w `.state/gmail_token.json` (ścieżka konfigurowalna
   przez `GMAIL_TOKEN_PATH`) i użyty automatycznie przy kolejnych
   uruchomieniach, bez ponownej autoryzacji w przeglądarce.
6. Filtr wiadomości domyślnie to `in:inbox -in:chats` (pomija wątki
   czatu); można go nadpisać zmienną `GMAIL_QUERY` (składnia jak w polu
   wyszukiwania Gmaila).

## Harmonogram (cron)

Agent sam się nie planuje — uruchamiaj go cyklicznie przez cron
maszyny, na której ma stale działać (serwer, własny komputer z
odpalonym cronem). Domyślny przykład: codziennie o 6:00 czasu
Europe/Warsaw.

1. Upewnij się, że `.venv` i `.env` są skonfigurowane (patrz wyżej) na
   maszynie docelowej.
2. Nadaj uprawnienia do wykonania (już ustawione w repo, ale po
   sklonowaniu może wymagać ponowienia):

       chmod +x scripts/run_daily.sh

3. `crontab -e` i wklej wpis z `cron/inbox-agent.cron.example`,
   podmieniając ścieżki na rzeczywistą lokalizację repozytorium.
4. Logi z każdego uruchomienia trafiają do `logs/cron.log`.

`scripts/run_daily.sh` ustawia `TZ=Europe/Warsaw` przed uruchomieniem,
więc data w nazwie pliku podsumowania jest poprawna niezależnie od
tego, czy cron respektuje `CRON_TZ`. Aby zmienić godzinę lub strefę,
edytuj `CRON_TZ=` i pole godziny (`0 6 * * *`) w crontabie oraz `TZ=`
w skrypcie.

## Dodanie kolejnego dostawcy poczty

1. Zaimplementuj klasę dziedziczącą po `inbox_agent.mail.base.MailProvider`
   (metoda `fetch_new_messages(since)`).
2. Podłącz ją w `inbox_agent/main.py::get_mail_provider`.
3. Dodaj wymagane zmienne konfiguracyjne do `.env.example` i `config.py`.
