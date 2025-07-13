from interfaces import cli

def main():
    """
    Janusz Danych Rodo - anonimizator danych w umowach
    
    source venv/bin/activate
    ===========================================
    - Uruchomienie z argumentami: interfejs CLI.
    
    Anonimizuj dokumenty z linii komend.
    
    opcje:
    -h, --help            pokaż pomoc i wyjdź
    -i INPUT, --input INPUT
                        ścieżka do pliku źródłowego
    -o OUTPUT, --output OUTPUT
                        ścieżka do pliku wyjściowego. Domyślnie <input>.anon.<ext>
    --profile {pseudonymized,gdpr,llm-safe}
                        profil anonimizacji
    --classes CLASSES [CLASSES ...]
                        lista klas do anonimizacji (nadpisuje ustawienia profilu)
    
    ===========================================
    """

cli.main()

if __name__ == "__main__":
    main()