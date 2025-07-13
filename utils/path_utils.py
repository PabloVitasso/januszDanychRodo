import os

def create_output_path(input_path, output_arg=None):
    """Generuje ścieżkę wyjściową jeśli nie podano"""
    if output_arg:
        return output_arg
    base, ext = os.path.splitext(input_path)
    return f"{base}.anon{ext}"

def create_map_path(input_path):
    """Generuje ścieżkę dla pliku mapy"""
    base, _ = os.path.splitext(input_path)
    return f"{base}.anon.map.json"