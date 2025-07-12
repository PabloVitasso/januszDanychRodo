# Definicje profili anonimizacji

PROFILES = {
    "pseudonymized": {
        "description": "Pseudonimizacja: Zamiana encji na tagi, z możliwością odwrócenia (generuje mapę).",
        "classes": ["PESEL", "NIP", "REGON", "KW", "PERSON", "LOCATION", "ORGANIZATION", "MONEY", "DATE"],
        "transformations": {
            "DATE": "tokenize",
            "MONEY": "tokenize"
        }
    },
    "gdpr": {
        "description": "Anonimizacja RODO: Nieodwracalna generalizacja danych.",
        "classes": ["PERSON", "LOCATION", "ORGANIZATION", "MONEY", "DATE"],
        "transformations": {
            "DATE": "generalize",
            "MONEY": "generalize",
            "PERSON": "remove",
            "LOCATION": "generalize_loc",
            "ORGANIZATION": "remove"
        }
    },
    "llm-safe": {
        "description": "Profil LLM-Safe: Maksymalna anonimizacja, zastępowanie semantyczne.",
        "classes": ["PESEL", "NIP", "REGON", "KW", "PERSON", "LOCATION", "ORGANIZATION", "MONEY", "DATE"],
        "transformations": {
            "DATE": "generalize",
            "MONEY": "generalize",
            "PERSON": "replace_semantic",
            "LOCATION": "replace_semantic",
            "ORGANIZATION": "replace_semantic"
        }
    }
}

DEFAULT_PROFILE = "pseudonymized"