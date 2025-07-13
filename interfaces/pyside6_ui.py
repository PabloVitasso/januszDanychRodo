import sys
import json

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QTextEdit, QFileDialog, QComboBox, QMessageBox
)

from core.anonymizer import anonymize_text
from core.profile_config import PROFILES


class AnonymizerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Janusz Danych RODO – Anonimizator Umów Notarialnych")
        self.setMinimumWidth(800)
        
        layout = QVBoxLayout()

        # Wybór pliku
        self.load_button = QPushButton("Wgraj plik (.txt, .md)")
        self.load_button.clicked.connect(self.load_file)
        layout.addWidget(self.load_button)

        # Profil anonimizacji
        self.profile_dropdown = QComboBox()
        self.profile_dropdown.addItems(PROFILES.keys())
        layout.addWidget(QLabel("Profil Anonimizacji"))
        layout.addWidget(self.profile_dropdown)

        # Przycisk anonimizacji
        self.anon_button = QPushButton("Anonimizuj")
        self.anon_button.clicked.connect(self.run_anonymization)
        layout.addWidget(self.anon_button)

        # Wyjście: zanonimizowany tekst
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(False)
        layout.addWidget(QLabel("Tekst zanonimizowany"))
        layout.addWidget(self.output_text)

        # Wyjście: słownik mapowań
        self.output_map = QTextEdit()
        self.output_map.setReadOnly(True)
        layout.addWidget(QLabel("Słownik mapowań"))
        layout.addWidget(self.output_map)

        # Przyciski pobierania
        self.save_map_btn = QPushButton("Zapisz słownik mapowań")
        self.save_map_btn.clicked.connect(self.save_map)
        layout.addWidget(self.save_map_btn)

        self.save_text_btn = QPushButton("Zapisz tekst anonimizowany")
        self.save_text_btn.clicked.connect(self.save_text)
        layout.addWidget(self.save_text_btn)

        self.setLayout(layout)
        self.file_content = None
        self.substitution_map = None
        self.anonymized_text = None

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik", "", "Text Files (*.txt *.md)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.file_content = f.read()
            QMessageBox.information(self, "Plik załadowany", "Wczytano plik.")

    def run_anonymization(self):
        if not self.file_content:
            QMessageBox.warning(self, "Błąd", "Nie wczytano pliku.")
            return

        profile = self.profile_dropdown.currentText()
        self.anonymized_text, self.substitution_map = anonymize_text(self.file_content, profile)

        self.output_text.setText(self.anonymized_text)
        self.output_map.setText(json.dumps(self.substitution_map, indent=2, ensure_ascii=False))

    def save_map(self):
        if not self.substitution_map:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Zapisz słownik mapowań", "mapowania.json", "JSON (*.json)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.substitution_map, f, ensure_ascii=False, indent=2)

    def save_text(self):
        if not self.anonymized_text:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Zapisz tekst anonimizowany", "tekst_anonimizowany.txt", "Text (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.anonymized_text)

def main():
    app = QApplication(sys.argv)
    window = AnonymizerGUI()
    window.show()
    sys.exit(app.exec())