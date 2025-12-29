import re

def validate_explanation(sentence, explanation_obj):
    """
    Ensures explanation is safe, non-prescriptive, and sentence-bound.
    """
    explanation_text = explanation_obj.get("explanation", "").lower()

    # ❌ Block explicit medical advice (imperative forms)
    forbidden_patterns = [
        r"\byou should\b",
        r"\byou must\b",
        r"\bwe recommend\b",
        r"\bconsult a doctor\b",
        r"\btake (this|that|it)\b",
        r"\bstart treatment\b",
        r"\bdosage\b"
    ]

    for pattern in forbidden_patterns:
        if re.search(pattern, explanation_text):
            raise ValueError("Unsafe medical advice detected")

    # ✅ Attach explanation safely
    sentence.explanation = explanation_obj["explanation"]
    return sentence
