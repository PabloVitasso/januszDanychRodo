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
    # Wzorzec dla kwot słownych, np. "sto tysięcy złotych"
    ("MONEY_TEXT", re.compile(r"""
        \b(
            (?:
                (?:jeden|dwa|trzy|cztery|pięć|sześć|siedem|osiem|dziewięć|dziesięć|
                jedenaście|dwanaście|trzynaście|czternaście|piętnaście|szesnaście|siedemnaście|osiemnaście|dziewiętnaście|
                dwadzieścia|trzydzieści|czterdzieści|pięćdziesiąt|sześćdziesiąt|siedemdziesiąt|osiemdziesiąt|dziewięćdziesiąt|
                sto|dwieście|trzysta|czterysta|pięćset|sześćset|siedemset|osiemset|dziewięćset|
                tysiąc|tysiące|tysięcy|milion|miliony|milionów|miliard|miliardy|miliardów)
                [\s,-]*
            )+
        )
        \s+(?:złotych|złote|złoty|pln|zł)\b
    """, re.IGNORECASE | re.VERBOSE)),
    ("MONEY", re.compile(r"(\d{1,3}(?:[ .]\d{3})*(?:,\d{2})?)\s?(z[łl])", re.IGNORECASE)),
    # Wzorce dla powierzchni. Najpierw bardziej szczegółowy (z opisem), potem ogólny.
    # To zapobiega sytuacji, w której ogólny wzorzec dopasowuje tylko część dłuższego wyrażenia.
    ("AREA", re.compile(r"""
        \b
        (?:ok\.\s*)?
        (?:
            (?:
                (?:\d{1,3}(?:[ .,]\d{3})*|\d+)(?:[,.]\d+)?\s*(?:ha|a|m²|m|cm²|cm|mm|km²)
            )
            (?:
                \s*(?:x\s*)?(?:\d{1,3}(?:[ .,]\d{3})*|\d+)(?:[,.]\d+)?\s*(?:a|m²|m|cm²|cm|mm|km²)
            ){0,2}
        )
        \s*\([^)]+\) # Opis w nawiasie jest tutaj obowiązkowy
    """, re.IGNORECASE | re.VERBOSE)),
    ("AREA", re.compile(r"""
        \b
        (?:ok\.\s*)?
        (?:
            (?:
                (?:\d{1,3}(?:[ .,]\d{3})*|\d+)(?:[,.]\d+)?\s*(?:ha|a|m²|m|cm²|cm|mm|km²)
            )
            (?:
                \s*(?:x\s*)?(?:\d{1,3}(?:[ .,]\d{3})*|\d+)(?:[,.]\d+)?\s*(?:a|m²|m|cm²|cm|mm|km²)
            ){0,2}
        )
        \b
    """, re.IGNORECASE | re.VERBOSE)),
    ("DATE", re.compile(r"\b\d{1,2}\.\d{1,2}\.\d{4}\b")),
    ("DATE", re.compile(r"\b\d{1,2} [a-zA-Z]+ \d{4} roku\b", re.IGNORECASE)),
    ("POST_CODE", re.compile(r"\b\d{2}-\d{3}\b")),
    ("STREET_ADDRESS", re.compile(r"""
        \b(
            (?:ul|al|pl|os)\.?\s+
            (?:[A-ZŻŹĆĄŚĘŁÓŃa-zżźćńółęąś-]+\s+)+
            \d{1,4}
            (?:[a-zA-Z])?
            (?:/\d{1,4})?
        )\b
    """, re.IGNORECASE | re.VERBOSE)),
    ("LAND_PLOT", re.compile(r"\b\d+\s*/\s*\d+\b")),
]