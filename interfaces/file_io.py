import json

def read_file(file_path: str) -> str:
    """Odczytuje zawartość pliku tekstowego."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Błąd: Plik nie został znaleziony: {file_path}")
        return ""

def write_file(file_path: str, content: str):
    """Zapisuje zawartość do pliku tekstowego."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def save_map_dict(file_path: str, substitution_dict: dict):
    """Zapisuje słownik mapowań do pliku JSON."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(substitution_dict, f, ensure_ascii=False, indent=2)