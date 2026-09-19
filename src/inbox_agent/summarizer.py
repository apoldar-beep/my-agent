from __future__ import annotations

from datetime import date

import anthropic

from inbox_agent.models import EmailMessage

SYSTEM_PROMPT = """Jesteś asystentem tworzącym poranne podsumowanie skrzynki odbiorczej.
Format wyjścia — jedna strona po polsku, w kolejności ważności:
1. Krótki nagłówek z datą i liczbą nowych wiadomości.
2. Lista punktowana najważniejszych wiadomości: nadawca, temat w 1 zdaniu,
   sugerowana akcja (odpowiedz / do wiadomości / termin).
3. Sekcja "Wymaga odpowiedzi dziś" na końcu, jeśli dotyczy.
Newslettery, powiadomienia automatyczne i spam pomiń albo zgrupuj w jednej linii.
Bez wstępu ani komentarza — same konkrety."""

MODEL = "claude-sonnet-5"


def build_summary(messages: list[EmailMessage], today: date, api_key: str) -> str:
    if not messages:
        return (
            f"# Podsumowanie skrzynki — {today.isoformat()}\n\n"
            "Brak nowych wiadomości od ostatniego uruchomienia."
        )

    client = anthropic.Anthropic(api_key=api_key)
    body = "\n\n".join(
        f"Od: {m.sender}\nTemat: {m.subject}\nTreść (fragment): {m.snippet}"
        for m in messages
    )
    user_content = (
        f"Data: {today.isoformat()}\n"
        f"Liczba nowych wiadomości: {len(messages)}\n\n{body}"
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )
    return response.content[0].text
