def run_pipeline(uploaded_file):
    from core.ingestion.loader import load_file
    from core.ingestion.text_cleaner import clean_text
    from core.structuring.sentence_splitter import split_sentences

    from core.confusion.readability import compute_readability
    from core.confusion.linguistic import compute_linguistic_features
    from core.confusion.jargon import detect_medical_jargon
    from core.confusion.undefined import detect_undefined_concepts
    from core.confusion.cognitive_load import compute_cognitive_load
    from core.confusion.classifier import classify_confusion

    from core.gap_bridge.prerequisite import build_prerequisite_payload
    from core.gap_bridge.explainer import generate_explanation
    from core.gap_bridge.validator import validate_explanation

    from core.scoring.confusion_delta import compute_confusion_delta
    from core.scoring.coverage import compute_prerequisite_coverage
    from core.scoring.readability_delta import compute_readability_delta
    from core.scoring.clarity_score import compute_clarity_score

    # 1. Load + clean
    raw_text = load_file(uploaded_file)
    cleaned_text = clean_text(raw_text)

    # 2. Sentence structuring
    sentences = split_sentences(cleaned_text)

    # 3. NLP confusion detection
    for s in sentences:
        compute_readability(s)
        compute_linguistic_features(s)
        detect_medical_jargon(s)
        detect_undefined_concepts(s)
        compute_cognitive_load(s)
        classify_confusion(s)

    # 4. Gemini explanations (only when needed)
    for s in sentences:
        payload = build_prerequisite_payload(s)
        if payload:
            explanation_obj = generate_explanation(payload)
            validate_explanation(s, explanation_obj)

    # 5. Clarity score
    confusion_delta = compute_confusion_delta(sentences)
    coverage = compute_prerequisite_coverage(sentences)
    readability = compute_readability_delta(sentences)
    clarity = compute_clarity_score(confusion_delta, coverage, readability)

    return sentences, clarity
