import sys
import json
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QTextEdit, QFileDialog, QMessageBox
)
from core.anonymizer import anonymize_text
from utils.path_utils import create_output_path, create_map_path
from core.branding import (
    APP_TITLE, L_FILE_UPLOAD, L_ANONYMIZE_BTN, L_OUTPUT_TEXT,
    L_SUBSTITUTION_MAP, L_SAVE_MAP_BTN, L_SAVE_TEXT_BTN
)

class AnonymizerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setMinimumWidth(800)
        
        layout = QVBoxLayout()
        
        # Wybór pliku
        self.load_button = QPushButton(L_FILE_UPLOAD)
        self.load_button.clicked.connect(self.load_file)
        layout.addWidget(self.load_button)
        
        # Label dla nazwy pliku
        self.file_label = QLabel("Brak pliku")
        layout.addWidget(self.file_label)
        
        # Przycisk anonimizacji
        self.anon_button = QPushButton(L_ANONYMIZE_BTN)
        self.anon_button.clicked.connect(self.run_anonymization)
        layout.addWidget(self.anon_button)
        
        # Wyjście: zanonimizowany tekst
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(False)
        layout.addWidget(QLabel(L_OUTPUT_TEXT))
        layout.addWidget(self.output_text)
        
        # Wyjście: słownik mapowań
        self.output_map = QTextEdit()
        self.output_map.setReadOnly(True)
        layout.addWidget(QLabel(L_SUBSTITUTION_MAP))
        layout.addWidget(self.output_map)
        
        # Przyciski pobierania
        self.save_map_btn = QPushButton(L_SAVE_MAP_BTN)
        self.save_map_btn.clicked.connect(self.save_map)
        layout.addWidget(self.save_map_btn)
        
        self.save_text_btn = QPushButton(L_SAVE_TEXT_BTN)
        self.save_text_btn.clicked.connect(self.save_text)
        layout.addWidget(self.save_text_btn)
        
        self.setLayout(layout)
        
        self.file_content = None
        self.substitution_map = None
        self.anonymized_text = None
        self.input_file_path = None
    

    
    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik", "", "Text Files (*.txt *.md)")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.file_content = f.read()
                self.input_file_path = file_path
                self.file_label.setText(os.path.basename(file_path))
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie można wczytać pliku: {e}")
    
    def run_anonymization(self):
        if not self.file_content:
            QMessageBox.warning(self, "Błąd", "Nie wczytano pliku.")
            return
        
        self.anonymized_text, self.substitution_map = anonymize_text(self.file_content)
        self.output_text.setText(self.anonymized_text)
        self.output_map.setText(json.dumps(self.substitution_map, indent=2, ensure_ascii=False))
    
    def save_map(self):
        if not self.substitution_map or not self.input_file_path:
            return
        
        default_path = create_map_path(self.input_file_path)
        path, _ = QFileDialog.getSaveFileName(self, "Zapisz słownik mapowań", default_path, "JSON (*.json)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.substitution_map, f, ensure_ascii=False, indent=2)
    
    def save_text(self):
        if not self.anonymized_text or not self.input_file_path:
            return
        
        default_path = create_output_path(self.input_file_path)
        _, ext = os.path.splitext(self.input_file_path)
        path, _ = QFileDialog.getSaveFileName(self, "Zapisz tekst anonimizowany", default_path, f"Text (*{ext})")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.anonymized_text)

def main():
    app = QApplication(sys.argv)
    window = AnonymizerGUI()
    window.show()
    sys.exit(app.exec())