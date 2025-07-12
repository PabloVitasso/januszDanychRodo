import re

# Wzorce Regex do identyfikacji danych wrażliwych

# Zmieniono na listę krotek, aby zachować kolejność przetwarzania
# Ważne: PESEL musi być przed REGON, aby uniknąć błędnego dopasowania
PATTERNS = [
    ("KW", re.compile(r"\b[A-Z]{2}[A-Z0-9]{2}/\d{8}/\d\b")),
    ("PESEL", re.compile(r"\b\d{11}\b")),
    ("NIP", re.compile(r"\b\d{3}[- ]?\d{3}[- ]?\d{2}[- ]?\d{2}\b")),
    ("REGON", re.compile(r"\b\d{9,14}\b")),
    # Poprawiony, prostszy wzorzec dla organizacji w cudzysłowach
    ("ORGANIZATION", re.compile(r'"([^"]+ S\.A\.)"', re.IGNORECASE)),
    ("MONEY", re.compile(r"(\d{1,3}(?:[ .]\d{3})*(?:,\d{2})?)\s?(z[łl])", re.IGNORECASE)),
    ("DATE", re.compile(r"\b\d{1,2}\.\d{1,2}\.\d{4}\b")),
    ("DATE", re.compile(r"\b\d{1,2} [a-zA-Z]+ \d{4} roku\b", re.IGNORECASE)),
]