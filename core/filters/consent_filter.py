# core/filters/consent_filter.py

import re

# -----------------------------
# Keyword configuration
# -----------------------------

CONSENT_KEYWORDS = [
    "consent",
    "authorization",
    "acknowledge",
    "agree",
    "permission",
    "voluntary",
    "right to",
    "risks",
    "hazards",
    "benefits",
    "withdraw",
    "privacy",
    "hipaa",
    "treatment",
    "procedure",
    "medical decision",
    "no guarantee",
    "revoked",
    "effective",
]

DROP_KEYWORDS = [
    "dob", "date of birth", "address", "zip", "phone", "email",
    "insurance", "policy", "billing", "payment",
    "pharmacy", "medical history", "medication",
    "allergies", "family history", "social history",
    "employment", "financial",
    "signature", "printed name", "witness",
    "checkbox", "yes / no", "❑", "____",
    "mrn", "policy#", "group id",
    "ssn", "fax", "employer"
]

# -----------------------------
# Helper functions
# -----------------------------

def split_on_sentence_boundaries(text: str):
    return re.split(r'(?<=[.!?])\s+', text)


def split_on_legal_boundaries(text: str):
    patterns = [
        r'\bBy signing\b',
        r'\bI understand\b',
        r'\bYou have the right\b',
        r'\bThis consent\b',
        r'\bThis authorization\b',
        r'\bI certify\b',
        r'\bI acknowledge\b'
    ]

    for p in patterns:
        text = re.sub(p, f'|||{p.strip("\\b")}', text)

    return [t.strip() for t in text.split("|||") if t.strip()]


def looks_like_form_noise(text: str) -> bool:
    if len(text.split()) < 8:
        return True

    alpha_ratio = sum(c.isalpha() for c in text) / max(len(text), 1)
    return alpha_ratio < 0.6


def looks_like_section_header(text: str) -> bool:
    return text.isupper() and len(text.split()) > 4


def looks_like_intake_question(text: str) -> bool:
    return text.strip().endswith("?") and len(text.split()) < 15


# -----------------------------
# Main filter (RETURNS LIST)
# -----------------------------

def filter_consent_text(raw_text: str):
    """
    Returns a LIST of clean, atomic consent sentences.
    This output is FINAL and must not be re-split later.
    """

    raw_lines = raw_text.split("\n")
    candidate_lines = []

    for l in raw_lines:
        parts = split_on_sentence_boundaries(l)
        for p in parts:
            candidate_lines.extend(split_on_legal_boundaries(p))

    kept_sentences = []

    for line in candidate_lines:
        original = line.strip()
        t = original.lower()

        if not original:
            continue

        if looks_like_section_header(original):
            continue

        if looks_like_form_noise(original):
            continue

        if looks_like_intake_question(original):
            continue

        if any(k in t for k in DROP_KEYWORDS):
            continue

        if any(k in t for k in CONSENT_KEYWORDS):
            kept_sentences.append(original)

    return kept_sentences
