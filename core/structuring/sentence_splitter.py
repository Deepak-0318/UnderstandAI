# core/structuring/sentence_splitter.py

import spacy
from .models import Sentence

nlp = spacy.load("en_core_web_sm")


def split_sentences(text_or_list):
    """
    If input is already a list of sentences (from consent filter),
    treat them as final. Otherwise, fall back to spaCy splitting.
    """

    sentences = []
    idx = 1

    # ✅ CASE 1: consent filter already produced atomic sentences
    if isinstance(text_or_list, list):
        for s in text_or_list:
            cleaned = s.strip()

            if not cleaned:
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

    # ❌ CASE 2: raw text fallback (should rarely happen now)
    doc = nlp(text_or_list)

    for sent in doc.sents:
        cleaned = sent.text.strip()

        if not cleaned:
            continue

        if cleaned.replace("_", "").strip() == "":
            continue

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
