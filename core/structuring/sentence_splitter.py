# core/structuring/sentence_splitter.py

import spacy
from .models import Sentence

nlp = spacy.load("en_core_web_sm")

def split_sentences(text: str):
    doc = nlp(text)
    sentences = []
    idx = 1

    for sent in doc.sents:
        cleaned = sent.text.strip()

        # ❌ Ignore empty or placeholder lines
        if not cleaned:
            continue

        if cleaned.replace("_", "").strip() == "":
            continue

        # ❌ Ignore extremely short fragments
        if len(cleaned.split()) < 4:
            continue

        sentences.append(
            Sentence(
                sentence_id=f"S{idx}",
                text=cleaned,
                position=idx
            )
        )
        idx += 1

    return sentences
