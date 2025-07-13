import os
import gradio as gr
from core.anonymizer import anonymize_text
import tempfile
import json
from core.branding import (
    APP_TITLE, L_FILE_UPLOAD, L_ANONYMIZE_BTN, L_OUTPUT_TEXT,
    L_SUBSTITUTION_MAP, L_DOWNLOAD_FILES
)

# Wyłącz analytics
os.environ['GRADIO_ANALYTICS_ENABLED'] = 'False'
os.environ['HF_HUB_OFFLINE'] = '1'

class AnonymizerInterface:
    """Wrapper dla interfejsu anonimizatora"""
    
    @staticmethod
    def create_temp_file(content, filename, extension):
        """Tworzy tymczasowy plik z contentem"""
        if not content:
            return None
        
        with tempfile.NamedTemporaryFile(
            delete=False,
            mode="w",
            suffix=extension,
            prefix=filename + "_",
            encoding="utf-8"
        ) as tmp:
            if extension == ".json":
                json.dump(content, tmp, ensure_ascii=False, indent=2)
            else:
                tmp.write(content)
            return tmp.name
    
    @staticmethod
    def process_file(file_obj):
        """Przetwarza plik i zwraca wyniki anonimizacji"""
        if file_obj is None:
            return "Proszę wgrać plik.", "Brak wyników.", None, None
        
        original_text = file_obj.decode('utf-8')
        anonymized_text, substitution_map = anonymize_text(original_text)
        
        # Tworzenie plików do pobrania
        map_file_path = AnonymizerInterface.create_temp_file(
            substitution_map,
            "mapowania",
            ".json"
        )
        
        text_file_path = AnonymizerInterface.create_temp_file(
            anonymized_text,
            "tekst_anonimizowany",
            ".txt"
        )
        
        return anonymized_text, substitution_map, map_file_path, text_file_path

def create_ui():
    """Tworzy interfejs użytkownika"""
    with gr.Blocks(
        css="""
        * {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif !important;
        }
        link[rel="manifest"] { display: none !important; }
        """,
        theme=gr.themes.Soft()
    ) as demo:
        
        gr.Markdown(f"# {APP_TITLE}")
        
        # Wiersz 1: Wgranie pliku, profil, przycisk
        with gr.Row():
            file_input = gr.File(
                label=L_FILE_UPLOAD,
                type="binary",
                file_count="single"
            )
            submit_btn = gr.Button(L_ANONYMIZE_BTN)
        
        # Wiersz 2: Tekst zanonimizowany
        with gr.Row():
            output_text = gr.Textbox(
                label=L_OUTPUT_TEXT,
                lines=15,
                interactive=True
            )
        
        # Wiersz 3: Słownik mapowań i pobieranie
        with gr.Row():
            with gr.Column():
                output_map = gr.JSON(label=L_SUBSTITUTION_MAP)
            
            with gr.Column():
                gr.Markdown(f"### {L_DOWNLOAD_FILES}")
                with gr.Group():
                    download_map_btn = gr.File(label=L_SUBSTITUTION_MAP)
                    download_text_btn = gr.File(label=L_OUTPUT_TEXT)
        
        submit_btn.click(
            fn=AnonymizerInterface.process_file,
            inputs=[file_input],
            outputs=[output_text, output_map, download_map_btn, download_text_btn]
        )
        
        return demo

def launch():
    """Uruchamia aplikację"""
    print("Working directory:", os.getcwd())
    print("Static dir exists:", os.path.exists("static"))
    print("Manifest exists:", os.path.exists("static/manifest.json"))
    print(gr.__version__)
    print(hasattr(gr, 'set_static_paths'))
    
    demo = create_ui()
    demo.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        quiet=True,
        show_error=True,
        favicon_path=None,
    )

if __name__ == "__main__":
    launch()