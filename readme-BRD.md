# Plan Projektu: System Anonimizacji Umów Notarialnych

Dokument ten stanowi ogólny plan wdrożenia (BRD+FRD) systemu do anonimizacji, uwzględniający specyfikację techniczną oraz kluczowe uwagi i poprawki. Jest to punkt wyjścia do szczegółowej specyfikacji kolejnych etapów prac, włączając Proof of Concept (POC) i testowanie.

## 1. Wprowadzenie i Cele

*   **Cel Główny**: Automatyczna, konfigurowalna anonimizacja polskich umów notarialnych w celu ochrony danych wrażliwych.
*   **Cele Biznesowe**:
    *   Zgodność z RODO przy przetwarzaniu dokumentów.
    *   Przygotowanie bezpiecznych danych do analiz (ML/LLM, analityka prawna).
    *   Umożliwienie bezpiecznej wymiany dokumentów z usuniętymi danymi osobowymi.
*   **Użytkownicy Docelowi**:
    *   Kancelarie notarialne i prawne.
    *   Developerzy, analitycy danych, sektor fintech.
    *   Instytucje badawcze.

## 2. Architektura Systemu i Moduły

Struktura projektu będzie modułowa, aby zapewnić elastyczność i łatwość w utrzymaniu.

```
.
├── core/                  # Główna logika
│   ├── anonymizer.py      # Silnik anonimizacji
│   ├── patterns.py        # Definicje regex dla identyfikatorów
│   ├── transforms.py      # Funkcje transformujące (np. kwoty na przedziały)
│   ├── normalizer.py      # Normalizacja stylu i języka
│   └── profile_config.py  # Konfiguracja profili (RODO, LLM-Safe)
├── interfaces/            # Interfejsy użytkownika
│   ├── cli.py             # Obsługa z linii poleceń
│   ├── gradio_ui.py       # Interfejs webowy Gradio
│   └── file_io.py         # Operacje na plikach (odczyt/zapis)
├── utils/                 # Narzędzia pomocnicze
│   ├── log.py             # Logowanie operacji
│   └── tokens.py          # Generator unikalnych tokenów
├── tests/                 # Testy jednostkowe i integracyjne
│   ├── test_anonymizer.py
│   └── test_patterns.py
├── main.py                # Punkt wejścia aplikacji
└── requirements.txt       # Zależności (spaCy, Gradio, etc.)
```

## 3. Wymagania Funkcjonalne

### 3.1. Przetwarzanie Danych

*   **Format wejściowy**: `.txt`, `.md`.
*   **Formaty wyjściowe**:
    *   `<nazwa>-anon.md`: Dokument zanonimizowany.
    *   `<nazwa>-mapa.json`: Słownik mapowań (dla pseudonimizacji).
    *   `<nazwa>.log`: Log zdarzeń i przeprowadzonych zmian.

### 3.2. Kategorie Anonimizacji

System musi identyfikować i przetwarzać następujące kategorie danych, łącząc wymagania ze `specyfikacja.txt` i `uwagi.md`:

1.  **Dane osobowe**: Imiona, nazwiska, nazwy podmiotów prawnych.
2.  **Adresy**: Ulice, miasta, kody pocztowe.
3.  **Lokalizacje geograficzne**: Województwa, regiony.
4.  **Identyfikatory**: PESEL, NIP, REGON.
5.  **Dane nieruchomości**: Numery ksiąg wieczystych (KW), numery działek.
6.  **Wartości liczbowe**: Powierzchnie, kwoty.
7.  **Daty**: Daty dzienne, miesięczne, roczne.
8.  **Styl i frazy**: Usuwanie specyficznych formułek ("Ja, notariusz...").
9.  **Metadane**: Usuwanie danych EXIF z osadzonych plików (w przyszłości).

### 3.3. Techniki Anonimizacji

*   **NER**: Wykorzystanie modelu `spaCy/pl_core_news_lg` do identyfikacji encji ogólnych (osoby, miejsca).
*   **Regex**: Użycie listy precyzyjnych wyrażeń regularnych o ustalonej kolejności do identyfikacji danych strukturalnych (PESEL, NIP, KW, nazwy firm). Kolejność zapobiega konfliktom (np. PESEL vs REGON).
*   **Bezpieczne Zastępowanie**: Stosowanie `re.sub()` z granicami słów (`\bpattern\b`) w celu uniknięcia błędnych zamian częściowych.
*   **Transformacje**: Generalizacja (np. `Kraków` -> `duże miasto`), zaokrąglanie/przedziały (dla kwot i powierzchni).
*   **Pseudonimizacja**: Zastępowanie encji unikalnymi, spójnymi tokenami (np. `Jan Kowalski` -> `OSOBA_A`).

### 3.4. Profile Anonimizacji

*   **Pseudonimizacja**: Domyślny tryb, zamienia encje na tagi (`<PER_1>`), generuje odwracalną mapę.
*   **Anonimizacja RODO**: Nieodwracalna generalizacja danych bez możliwości odtworzenia oryginału.
*   **LLM-Safe**: Zastępowanie encji semantycznymi odpowiednikami, ukrywanie stylu i metadanych.

## 4. Plan Realizacji i Testowania

### Etap 1: Proof of Concept (POC)

*   **Cel**: Weryfikacja kluczowych założeń technicznych i skuteczności podejścia.
*   **Zakres**:
    1.  Implementacja podstawowego `core/anonymizer.py`.
    2.  Zastosowanie `re.sub()` dla 2-3 kluczowych kategorii (np. PESEL, KW, NIP).
    3.  Integracja ze `spaCy` do identyfikacji osób i lokalizacji.
    4.  Utworzenie prostego interfejsu CLI do testowania.
*   **Kryteria sukcesu**: Poprawna identyfikacja i anonimizacja wybranych encji w 2-3 przykładowych dokumentach.

### Etap 2: Rozwój MVP

*   **Cel**: Dostarczenie w pełni funkcjonalnej wersji produktu.
*   **Zakres**:
    1.  Implementacja wszystkich modułów z `core`, `utils`.
    2.  Kompletne `patterns.py` dla wszystkich zdefiniowanych kategorii.
    3.  Implementacja wszystkich profili anonimizacji.
    4.  W pełni funkcjonalne interfejsy CLI i Gradio.
    5.  Implementacja zapisu wszystkich plików wyjściowych.

### Etap 3: Testowanie i Walidacja

*   **Testy jednostkowe**: Pokrycie kluczowych funkcji w `core` i `utils`.
*   **Testy integracyjne**: Weryfikacja przepływu danych między interfejsami a silnikiem anonimizacji.
*   **Testy E2E**: Przetwarzanie realnych, zróżnicowanych umów notarialnych w celu walidacji skuteczności.
*   **Walidacja prawna**: Konsultacja w celu potwierdzenia zgodności profilu "RODO" z wymogami prawnymi.

## 5. Kluczowe Uwagi i Ryzyka

*   **Jakość NER**: Model `spaCy` może wymagać rozbudowanego zestawu reguł własnych, aby skutecznie działać na języku prawnym.
*   **Złożoność dokumentów**: Różnorodność formatowania i unikalne sformułowania w aktach notarialnych stanowią wyzwanie.
*   **Nieodwracalność**: Należy zagwarantować, że profil "Anonimizacja RODO" faktycznie uniemożliwia reidentyfikację.
*   **Wydajność**: Przetwarzanie bardzo dużych plików może wymagać optymalizacji.

## 6. Plan Rozwoju (Wersje Przyszłe)

*   **v1.1**: Obsługa formatu `.pdf` (z wykorzystaniem bibliotek do ekstrakcji tekstu).
*   **v2.0**: Wdrożenie mechanizmów k-anonimizacji.
*   **v2.1**: Użycie lokalnej bazy danych (np. SQLite) do zarządzania powtarzalnymi encjami i mapowaniami.