import sys
from interfaces import cli, gradio_ui

def main():
    """
    Główny punkt wejścia do aplikacji.

    - Uruchomienie z argumentami: interfejs CLI.
      Przykład: python main.py --input in.txt --output out.md

    - Uruchomienie bez argumentów: interfejs webowy Gradio.
      Przykład: python main.py
    """
    if len(sys.argv) > 1:
        # Tryb CLI, jeśli podano jakiekolwiek argumenty
        cli.main()
    else:
        # Tryb Gradio (GUI)
        print("Uruchamianie interfejsu Gradio... Otwórz przeglądarkę pod adresem http://127.0.0.1:7860")
        gradio_ui.launch()

if __name__ == "__main__":
    main()