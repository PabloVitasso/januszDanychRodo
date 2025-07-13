import logging
import os
import sys
from datetime import datetime

def setup_logger(input_filename: str = "session"):
    """
    Konfiguruje logger do zapisu w pliku w folderze ./logs.
    Nazwa pliku logu bazuje na dacie i nazwie pliku wejściowego.
    """
    LOG_LEVEL = logging.INFO # !!1 logging.DEBUG zapisuje DANE WRAŻLIWE do katalogu ./logs !!1
    
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    base_name = os.path.basename(input_filename)
    log_filename = f"{timestamp}-{base_name}.log"
    log_filepath = os.path.join(logs_dir, log_filename)
    
    # Tworzenie nowego loggera
    logger_name = f"app_{timestamp}_{base_name}"
    logger = logging.getLogger(logger_name)
    logger.setLevel(LOG_LEVEL)
    
    # Sprawdź czy handlery już istnieją
    if logger.handlers:
        return logger
    
    # File handler
    file_handler = logging.FileHandler(log_filepath, mode='w')
    file_handler.setLevel(LOG_LEVEL)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)
    
    # Formatters
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Globalna instancja loggera
logger = setup_logger()