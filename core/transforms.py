import re

def generalize_money(text: str) -> dict:
    """
    Generalizuje kwoty pieniężne, zastępując je przedziałami.
    Przykład: 521 000,00 zł -> około 500-550 tys. PLN
    """
    # Prosty regex dla kwot, można go rozwijać
    pattern = re.compile(r"(\d{1,3}(?:[ .]\d{3})*(?:,\d{2})?)\s?(z[łl])", re.IGNORECASE)
    substitution_dict = {}
    
    for match in pattern.finditer(text):
        original_string = match.group(0)
        numeric_part = match.group(1).replace(" ", "").replace(".", "")
        value = float(numeric_part.replace(",", "."))
        
        if value > 1_000_000:
            rounded = round(value / 100_000) * 100_000
            replacement = f"ponad {rounded / 1_000_000:.1f} mln PLN"
        elif value > 10_000:
            rounded = round(value / 10_000) * 10_000
            replacement = f"około {rounded/1000:.0f} tys. PLN"
        else:
            replacement = "poniżej 10 tys. PLN"
            
        if original_string not in substitution_dict:
            substitution_dict[original_string] = replacement
            
    return substitution_dict

def generalize_dates(text: str) -> dict:
    """
    Generalizuje daty do kwartałów lub miesięcy.
    Przykład: 12.03.2023 -> Q1 2023
    """
    pattern = re.compile(r"\b(\d{1,2})[./-](\d{1,2})[./-](\d{4})\b")
    substitution_dict = {}
    
    for match in pattern.finditer(text):
        original_string = match.group(0)
        _, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
        
        if 1 <= month <= 3:
            quarter = "Q1"
        elif 4 <= month <= 6:
            quarter = "Q2"
        elif 7 <= month <= 9:
            quarter = "Q3"
        else:
            quarter = "Q4"
            
        replacement = f"{quarter} {year}"
        if original_string not in substitution_dict:
            substitution_dict[original_string] = replacement
            
    return substitution_dict