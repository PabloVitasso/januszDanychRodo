# Anonymizer Notarialny

**Stan projektu: MVP 1 (Minimum Viable Product)**

Projekt aplikacji do anonimizacji polskich aktów notarialnych. Aplikacja identyfikuje i anonimizuje dane wrażliwe, takie jak dane osobowe, numery identyfikacyjne (PESEL, NIP), adresy i inne, zgodnie z wybranym profilem anonimizacji.

## Funkcjonalności

*   **Rozpoznawanie encji**: Wykorzystuje hybrydowe podejście (Regex + NER ze spaCy) do identyfikacji danych.
*   **Profile anonimizacji**:
    *   `pseudonymized`: Zamienia dane na tokeny (np. `Jan Kowalski` -> `<PERSON_0>`).
    *   `gdpr`: Generalizuje lub usuwa dane (np. `5000 zł` -> `[KWOTA]`).
    *   `llm-safe`: Profil przygotowany do bezpiecznego przetwarzania przez duże modele językowe.
*   **Interfejsy**:
    *   CLI (Command Line Interface) do przetwarzania plików.
    *   **PLANOWANE**: Web UI (Gradio) do interaktywnej anonimizacji tekstu.
*   **Logowanie**: Zapisuje szczegółowe logi z każdej sesji do katalogu `./logs`.

## Instalacja

1.  **Sklonuj repozytorium:**
    ```bash
    git clone [adres-repozytorium]
    cd [nazwa-katalogu]
    ```

2.  **Utwórz i aktywuj wirtualne środowisko:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Zainstaluj zależności:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Pobierz model językowy spaCy:**
    ```bash
    python -m spacy download pl_core_news_lg
    ```

## Użycie

### Interfejs Linii Poleceń (CLI)

```bash
python3 main.py cli --input-file [sciezka_do_pliku_wejsciowego] --output-file [sciezka_do_pliku_wyjsciowego] --profile [nazwa_profilu]
```
*   `--input-file`: Ścieżka do pliku tekstowego do anonimizacji.
*   `--output-file`: Ścieżka do zapisu zanonimizowanego tekstu.
*   `--profile`: Profil anonimizacji (`pseudonymized`, `gdpr`, `llm-safe`). Domyślnie `pseudonymized`.

### Interfejs Webowy (Gradio) - PLANOWANE

Aby uruchomić interfejs webowy, uruchom polecenie:
```bash
python3 main.py web
```
Aplikacja będzie dostępna pod adresem `http://127.0.0.1:7860`.