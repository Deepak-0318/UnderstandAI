COMMON_KNOWLEDGE_TERMS = {
    "infection",
    "therapy",
    "procedure"
}

def detect_undefined_concepts(sentence):
    medical_terms = sentence.metrics.get("medical_terms", [])

    undefined = []
    for term in medical_terms:
        if term not in COMMON_KNOWLEDGE_TERMS:
            undefined.append(term)

    sentence.metrics["undefined_concepts"] = undefined
    sentence.metrics["undefined_concept_count"] = len(undefined)

    return sentence
