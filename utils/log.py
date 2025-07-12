import logging
import os
from datetime import datetime

def setup_logger(input_filename: str = "session"):
    """
    Konfiguruje logger do zapisu w pliku w folderze ./logs.
    Nazwa pliku logu bazuje na dacie i nazwie pliku wejściowego.
    """
    # Utwórz folder logs, jeśli nie istnieje
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    # Przygotuj nazwę pliku
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    base_name = os.path.basename(input_filename)
    log_filename = f"{timestamp}-{base_name}.log"
    log_filepath = os.path.join(logs_dir, log_filename)

    # Konfiguracja loggera
    # Usuwamy poprzednie handlery, aby uniknąć duplikacji logów
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_filepath,
        filemode='w'
    )
    
    # Dodanie konsoli, aby widzieć logi na bieżąco
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    return logging.getLogger(__name__)

# Inicjalizacja domyślnego loggera
logger = setup_logger()