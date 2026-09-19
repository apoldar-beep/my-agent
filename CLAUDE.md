# Agent: Poranne podsumowanie skrzynki odbiorczej

## Cel
Codziennie rano przeczytaj nieprzeczytane / nowe wiadomości ze skrzynki
odbiorczej użytkownika i przygotuj jednostronicowe podsumowanie
najważniejszych rzeczy.

## Zanim zaczniesz
Nie zakładaj żadnej konkretnej konfiguracji (dostawcy poczty, API,
uwierzytelniania, strefy czasowej, godziny uruchomienia). Jeśli którejś
z tych rzeczy brakuje albo nie da się jej wywnioskować z repo/env,
zapytaj użytkownika zamiast zgadywać.

## Zakres podsumowania
- Uwzględniaj tylko wiadomości nowe od ostatniego uruchomienia (unikaj
  duplikatów dnia poprzedniego).
- Priorytetyzuj: pilne prośby, terminy/deadline'y, wiadomości od ważnych
  kontaktów, sprawy wymagające odpowiedzi.
- Pomijaj lub grupuj w jednej linii: newslettery, powiadomienia
  automatyczne, spam/promocje.

## Format wyjścia
Jedna strona, po polsku, w kolejności ważności:
1. Krótki nagłówek z datą i liczbą nowych wiadomości.
2. Lista punktowana najważniejszych wiadomości: nadawca, temat w 1
   zdaniu, sugerowana akcja (odpowiedz / do wiadomości / termin).
3. Sekcja "Wymaga odpowiedzi dziś" na końcu, jeśli dotyczy.
Bez zbędnego wstępu ani komentarza — same konkrety.

## Bezpieczeństwo i prywatność
- Treść skrzynki to dane wrażliwe użytkownika — nie wysyłaj jej ani
  fragmentów do żadnych zewnętrznych usług poza tym, co jest niezbędne
  do wygenerowania podsumowania.
- Nie podejmuj akcji na skrzynce (nie odpowiadaj, nie usuwaj, nie
  archiwizuj) bez wyraźnej zgody użytkownika — tylko czytaj i
  podsumowuj.
- Nie zgaduj adresu e-mail użytkownika ani danych logowania — pobieraj
  je tylko z jawnie skonfigurowanego źródła.

## Uruchomienie i rozwój
Instalacja, komendy (`pytest`, `python -m inbox_agent.main`) i struktura
kodu — patrz README.md.

## Rozwój agenta
Ten plik opisuje tylko pierwsze zadanie agenta. Kolejne funkcje
(np. odpowiadanie na maile, integracja z kalendarzem) dodawaj tu jako
nowe sekcje, dopiero gdy zostaną potwierdzone przez użytkownika.
