def compute_confusion_delta(sentences):
    """
    Measures reduction in confusion for explained sentences.
    """
    before = 0.0
    after = 0.0

    for s in sentences:
        load = s.metrics.get("cognitive_load_score", 0)
        before += load

        if s.explanation:
            # Explanation reduces perceived confusion
            after += load * 0.3   # 70% reduction assumption
        else:
            after += load

    return {
        "before_confusion": round(before, 2),
        "after_confusion": round(after, 2)
    }
