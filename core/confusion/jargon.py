import json
from pathlib import Path

MEDICAL_TERMS_PATH = Path("data/medical_terms.json")

with open(MEDICAL_TERMS_PATH, "r") as f:
    MEDICAL_TERMS = [term.lower() for term in json.load(f)]


def detect_medical_jargon(sentence):
    text = sentence.text.lower()

    found_terms = [term for term in MEDICAL_TERMS if term in text]

    sentence.metrics["medical_terms"] = found_terms
    sentence.metrics["medical_term_count"] = len(found_terms)

    word_count = sentence.metrics.get("word_count", len(text.split()))
    sentence.metrics["medical_jargon_density"] = (
        len(found_terms) / word_count if word_count else 0
    )

    return sentence
