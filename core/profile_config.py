# Definicje profili anonimizacji

PROFILES = {
    "pseudonymized": {
        "description": "Pseudonimizacja: Zamiana encji na tagi, z możliwością odwrócenia (generuje mapę).",
        "classes": [
            "PESEL", "NIP", "REGON", "KW", "PERSON", "LOCATION", "ORGANIZATION",
            "MONEY", "MONEY_TEXT", "DATE", "POST_CODE", "STREET_ADDRESS", "LAND_PLOT", "AREA"
        ],
        "transformations": {
            "DATE": "tokenize",
            "POST_CODE": "tokenize",
            "STREET_ADDRESS": "tokenize",
            "LAND_PLOT": "tokenize",
            "MONEY": "tokenize",
            "MONEY_TEXT": "tokenize",
            "AREA": "tokenize"
        }
    },
    "gdpr": {
        "description": "Anonimizacja RODO: Nieodwracalna generalizacja danych.",
        "classes": ["PERSON", "LOCATION", "ORGANIZATION", "MONEY", "MONEY_TEXT", "DATE", "POST_CODE", "STREET_ADDRESS", "LAND_PLOT"],
        "transformations": {
            "DATE": "generalize",
            "POST_CODE": "remove",
            "STREET_ADDRESS": "remove",
            "LAND_PLOT": "remove",
            "MONEY": "generalize",
            "MONEY_TEXT": "generalize",
            "PERSON": "remove",
            "LOCATION": "generalize_loc",
            "ORGANIZATION": "remove"
        }
    },
    "llm-safe": {
        "description": "Profil LLM-Safe: Maksymalna anonimizacja, zastępowanie semantyczne.",
        "classes": ["PESEL", "NIP", "REGON", "KW", "PERSON", "LOCATION", "ORGANIZATION", "MONEY", "MONEY_TEXT", "DATE", "POST_CODE", "STREET_ADDRESS", "LAND_PLOT"],
        "transformations": {
            "DATE": "generalize",
            "POST_CODE": "tokenize",
            "STREET_ADDRESS": "tokenize",
            "LAND_PLOT": "tokenize",
            "MONEY": "generalize",
            "MONEY_TEXT": "generalize",
            "PERSON": "replace_semantic",
            "LOCATION": "replace_semantic",
            "ORGANIZATION": "replace_semantic"
        }
    }
}

DEFAULT_PROFILE = "pseudonymized"