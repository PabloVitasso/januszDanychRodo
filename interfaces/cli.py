import argparse
import os
from core.anonymizer import anonymize_text
from .file_io import read_file, write_file, save_map_dict
from utils.log import setup_logger

def main():
    parser = argparse.ArgumentParser(description="Anonymize documents from the command line.")
    parser.add_argument("-i", "--input", required=True, help="Path to the source file.")
    parser.add_argument("-o", "--output", help="Path to the output anonymized file. Defaults to <input>.anon.<ext>")
    parser.add_argument("--profile", default="pseudonymized", choices=["pseudonymized", "gdpr", "llm-safe"],
                        help="Anonymization profile.")
    
    # Opcja --classes staje się opcjonalna - nadpisuje ustawienia z profilu
    parser.add_argument("--classes", nargs='+', default=None,
                        help="Custom list of classes to anonymize (overwrites profile setting).")
    
    args = parser.parse_args()

    # Jeśli plik wyjściowy nie jest podany, utwórz go na podstawie nazwy pliku wejściowego
    if not args.output:
        base, ext = os.path.splitext(args.input)
        args.output = f"{base}.anon{ext}"

    # Skonfiguruj logger z nazwą pliku wejściowego
    logger = setup_logger(args.input)

    # Odczyt pliku
    original_text = read_file(args.input)
    if not original_text:
        return

    # Anonimizacja
    logger.info(f"Starting anonymization for {args.input} using profile: {args.profile}...")
    anonymized_text, substitution_map = anonymize_text(original_text, args.profile, args.classes)

    # Zapis wyników
    write_file(args.output, anonymized_text)
    
    map_file_path = args.output.rsplit('.', 1)[0] + '_map.json'
    if substitution_map:
        save_map_dict(map_file_path, substitution_map)
        logger.info(f"Anonymization complete. Output saved to: {args.output}")
        logger.info(f"Substitution map saved to: {map_file_path}")
    else:
        logger.info("No tokenized entities found to create a map.")

if __name__ == "__main__":
    main()