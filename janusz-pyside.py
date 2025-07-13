import sys
from interfaces import pyside6_ui


def check_venv():
    """
    Sprawdza, czy uruchomiono w środowisku wirtualnym.
    Jeśli nie – ostrzega użytkownika.
    """
    if sys.prefix == sys.base_prefix:
        print("[OSTRZEŻENIE] Aplikacja działa tylko w środowisku wirtualnym (venv).")
        print("Użyj:  source venv/bin/activate  (Linux/macOS)")
        print("       .\\venv\\Scripts\\activate  (Windows)")
        print("-" * 50)


def main():
    """
    Janusz Danych Rodo – wersja desktopowa (PySide6)

    Uruchamia aplikację jako natywne GUI.
    """
    check_venv()
    pyside6_ui.main()


if __name__ == "__main__":
    main()
