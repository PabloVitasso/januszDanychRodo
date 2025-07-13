from interfaces import gradio_ui

import os
os.environ['GRADIO_ANALYTICS_ENABLED'] = 'False'
os.environ['HF_HUB_OFFLINE'] = '1'

def main():
    """
    Janusz Danych Rodo - anonimizator danych w umowach
    
    source venv/bin/activate
    ===========================================
    interfejs webowy Gradio.

    strona uruchomi się pod adresem http://127.0.0.1:7860
    """
gradio_ui.launch()

if __name__ == "__main__":
    main()