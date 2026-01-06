def build_prerequisite_payload(sentence):
    """
    Prepares input for Gemini based on detected gaps.
    """
    if sentence.confusion_label not in ("HIGH", "MEDIUM"):
        return None

    undefined = sentence.metrics.get("undefined_concepts", [])
    if not undefined:
        return None

    return {
        "sentence_id": sentence.sentence_id,
        "original_sentence": sentence.text,
        "missing_concepts": undefined
    }
