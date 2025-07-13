# Configuration for the anonymizer
DEFAULT_CLASSES = [
    "PESEL", "NIP", "REGON", "KW", "PERSON", "LOCATION", "ORGANIZATION",
    "MONEY", "MONEY_TEXT", "DATE", "POST_CODE", "STREET_ADDRESS", "LAND_PLOT", "AREA"
]

DEFAULT_TRANSFORMATIONS = {
    "DATE": "tokenize",
    "POST_CODE": "tokenize",
    "STREET_ADDRESS": "tokenize",
    "LAND_PLOT": "tokenize",
    "MONEY": "tokenize",
    "MONEY_TEXT": "tokenize",
    "AREA": "tokenize"
}