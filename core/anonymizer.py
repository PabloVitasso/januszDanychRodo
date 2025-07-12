from typing import NamedTuple, Dict, Set
import spacy
from .patterns import PATTERNS
from .transforms import generalize_money, generalize_dates
from .profile_config import PROFILES, DEFAULT_PROFILE
from utils.log import logger

class Entity(NamedTuple):
    text: str
    type: str
    start: int
    end: int

# Ładowanie modelu spaCy
try:
    nlp = spacy.load("pl_core_news_lg")
except OSError:
    logger.error("Nie znaleziono modelu 'pl_core_news_lg'. Uruchom:\npython -m spacy download pl_core_news_lg")
    nlp = None

def safe_substitute(text: str, substitution_dict: dict) -> str:
    sorted_keys = sorted(substitution_dict.keys(), key=len, reverse=True)
    for original in sorted_keys:
        replacement = substitution_dict[original]
        text = text.replace(original, replacement)
    return text

def anonymize_text(text: str, profile: str = DEFAULT_PROFILE, custom_classes: list[str] = None) -> tuple[str, dict]:
    profile_config = PROFILES.get(profile, PROFILES[DEFAULT_PROFILE])
    enabled_classes = custom_classes if custom_classes is not None else profile_config["classes"]
    transformations = profile_config.get("transformations", {})
    
    all_entities: list[Entity] = []
    
    # Krok 1: Znajdź wszystkie encje z REGEX i zapisz ich pozycje
    logger.debug("--- Regex Entity Recognition ---")
    matched_pos: Set[range] = set()

    for class_name, pattern in PATTERNS:
        for match in pattern.finditer(text):
            start, end = match.span()
            # Sprawdź, czy zakres się nie nakłada
            if not any(start in r or end - 1 in r for r in matched_pos):
                entity = Entity(match.group(0), class_name, start, end)
                all_entities.append(entity)
                matched_pos.add(range(start, end))
                logger.debug(f"Regex found: {entity}")

    # Krok 2: Znajdź encje z NER, ignorując te, które nakładają się na regex
    logger.debug("--- NER Entity Recognition ---")
    if nlp:
        doc = nlp(text)
        ner_map = {"persName": "PERSON", "placeName": "LOCATION", "orgName": "ORGANIZATION"}
        for ent in doc.ents:
            start, end = ent.start_char, ent.end_char
            if not any(start in r or end - 1 in r for r in matched_pos):
                entity_type = ner_map.get(ent.label_)
                if entity_type:
                    entity = Entity(ent.text.strip(), entity_type, start, end)
                    all_entities.append(entity)
                    matched_pos.add(range(start, end))
                    logger.debug(f"NER found: {entity}")

    # Krok 3: Sortuj wszystkie znalezione encje wg pozycji startowej
    all_entities.sort(key=lambda x: x.start)
    logger.debug(f"All entities sorted by position: {[e.text for e in all_entities]}")

    # Krok 4: Zbuduj słownik zamian
    substitution_dict: Dict[str, str] = {}
    token_counters: Dict[str, int] = {}

    for entity in all_entities:
        if entity.type in enabled_classes:
            transform_type = transformations.get(entity.type, "tokenize")
            
            if transform_type == "tokenize":
                count = token_counters.get(entity.type, 0)
                substitution_dict[entity.text] = f"<{entity.type}_{count}>"
                token_counters[entity.type] = count + 1
            elif transform_type == "remove":
                substitution_dict[entity.text] = ""
            elif transform_type == "generalize_loc":
                 substitution_dict[entity.text] = "[MIASTO WOJEWÓDZKIE]"
            elif transform_type == "generalize":
                if entity.type == "MONEY":
                    substitution_dict.update(generalize_money(entity.text))
                elif entity.type == "DATE":
                    substitution_dict.update(generalize_dates(entity.text))
    
    if profile == 'gdpr':
        # Dodatkowe generalizacje dla GDPR
        temp_text = safe_substitute(text, substitution_dict)
        substitution_dict.update(generalize_dates(temp_text))
        substitution_dict.update(generalize_money(temp_text))

    anonymized_text = safe_substitute(text, substitution_dict)
    token_map = {v: k for k, v in substitution_dict.items() if v.startswith('<')}
    return anonymized_text, token_map
