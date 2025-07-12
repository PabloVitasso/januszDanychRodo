import gradio as gr
from core.anonymizer import anonymize_text
import tempfile
import json

from core.profile_config import PROFILES

def anonymize_interface(file_obj, profile):
    if file_obj is None:
        return "Proszę wgrać plik.", "Brak wyników.", None

    original_text = file_obj.decode('utf-8')
    
    anonymized_text, substitution_map = anonymize_text(original_text, profile)
    
    # Tworzenie pliku do pobrania
    if substitution_map:
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json", encoding="utf-8") as tmp:
            json.dump(substitution_map, tmp, ensure_ascii=False, indent=2)
            map_file_path = tmp.name
    else:
        map_file_path = None
        
    return anonymized_text, substitution_map, map_file_path

def launch():
    with gr.Blocks() as demo:
        gr.Markdown("# Anonimizator Umów Notarialnych")
        
        with gr.Row():
            with gr.Column():
                file_input = gr.File(label="Wgraj plik (.txt, .md)", type="binary")
                profile_dropdown = gr.Dropdown(
                    choices=list(PROFILES.keys()),
                    value="pseudonymized",
                    label="Profil Anonimizacji"
                )
                submit_btn = gr.Button("Anonimizuj")
            
            with gr.Column():
                output_text = gr.Textbox(label="Tekst zanonimizowany", lines=15)
                output_map = gr.JSON(label="Słownik mapowań")
                download_map_btn = gr.File(label="Pobierz słownik mapowań")

        submit_btn.click(
            fn=anonymize_interface,
            inputs=[file_input, profile_dropdown],
            outputs=[output_text, output_map, download_map_btn]
        )
    
    demo.launch()

if __name__ == "__main__":
    launch()