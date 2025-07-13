import argparse
import os
import sys
from core.anonymizer import anonymize_text
from .file_io import read_file, write_file, save_map_dict
from utils.log import setup_logger
from utils.path_utils import create_output_path, create_map_path
from core.branding import APP_NAME, APP_DESCRIPTION, VERSION

def create_parser():
    """Tworzy parser argumentów"""
    parser = argparse.ArgumentParser(description=APP_NAME+ ' '+VERSION+' - '+APP_DESCRIPTION)
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {VERSION}')
    parser.add_argument("-i", "--input", required=True, help="Ścieżka do pliku źródłowego.")
    parser.add_argument("-o", "--output", help="Ścieżka do pliku wyjściowego. Domyślnie <input>.anon.<ext>")
    return parser

def main():
    if len(sys.argv) == 1:
        parser = create_parser()
        parser.print_help()
        return
    
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.input:
        parser.print_help()
        return
    
    output_path = create_output_path(args.input, args.output)
    logger = setup_logger(args.input)
    
    original_text = read_file(args.input)
    if not original_text:
        return
    
    logger.info(f"Rozpoczęcie anonimizacji dla {args.input}...")
    anonymized_text, substitution_map = anonymize_text(original_text)
    
    write_file(output_path, anonymized_text)
    
    map_file_path = create_map_path(args.input)
    if substitution_map:
        save_map_dict(map_file_path, substitution_map)
        logger.info(f"Anonimizacja zakończona. Wynik zapisany w: {output_path}")
        logger.info(f"Mapa substytucji zapisana w: {map_file_path}")
    else:
        logger.info("Brak tokenizowanych jednostek do utworzenia mapy.")

if __name__ == "__main__":
    main()