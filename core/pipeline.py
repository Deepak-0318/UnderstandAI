def run_pipeline(uploaded_file):
    from core.ingestion.loader import load_file
    from core.ingestion.text_cleaner import clean_text, fix_line_wrapping
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

    from core.filters.consent_filter import filter_consent_text

    # --------------------------------------------------
    # 1. Load + clean text
    # --------------------------------------------------
    raw_text = load_file(uploaded_file)
    cleaned_text = clean_text(raw_text)
    cleaned_text = fix_line_wrapping(cleaned_text)

    # --------------------------------------------------
    # 2. Consent-only filtering (FINAL TEXT UNITS)
    # --------------------------------------------------
    consent_text = filter_consent_text(cleaned_text)

    # --------------------------------------------------
    # 3. Sentence structuring
    # --------------------------------------------------
    sentences = split_sentences(consent_text)

    # 🔒 Guard: no usable sentences
    if not sentences:
        return [], 0

    # 🔒 Guard: cap sentence count for stability
    MAX_SENTENCES = 120
    if len(sentences) > MAX_SENTENCES:
        sentences = sentences[:MAX_SENTENCES]

    # --------------------------------------------------
    # 4. NLP confusion detection (DETERMINISTIC)
    # --------------------------------------------------
    for s in sentences:
        compute_readability(s)
        compute_linguistic_features(s)
        detect_medical_jargon(s)
        detect_undefined_concepts(s)
        compute_cognitive_load(s)
        classify_confusion(s)

    # --------------------------------------------------
    # 5. Gemini explanations (STRICT + SAFE)
    # --------------------------------------------------
    for s in sentences:
        if s.confusion_label not in ("HIGH", "MEDIUM"):
            continue

        payload = build_prerequisite_payload(s)
        if not payload:
            continue

        try:
            explanation_obj = generate_explanation(payload)
            validate_explanation(s, explanation_obj)
        except Exception:
            # ❄️ Fail silently — never crash pipeline
            s.explanation = None

    # --------------------------------------------------
    # 6. Clarity score computation
    # --------------------------------------------------
    confusion_delta = compute_confusion_delta(sentences)
    coverage_pct = compute_prerequisite_coverage(sentences)
    readability_delta = compute_readability_delta(sentences)

    clarity = compute_clarity_score(
        confusion_delta,
        coverage_pct,
        readability_delta
    )

    return sentences, clarity
