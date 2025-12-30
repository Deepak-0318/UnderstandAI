def compute_clarity_score(confusion_delta, coverage_pct, readability_delta):
    """
    Produces final clarity score (0–100)
    """

    # -----------------------------
    # Confusion improvement
    # -----------------------------
    confusion_improvement = (
        (confusion_delta["before_confusion"] - confusion_delta["after_confusion"])
        / max(confusion_delta["before_confusion"], 1)
    )

    # -----------------------------
    # Readability improvement
    # -----------------------------
    readability_improvement = (
        (readability_delta["before_grade"] - readability_delta["after_grade"])
        / max(readability_delta["before_grade"], 1)
    )

    # -----------------------------
    # Weighted score (raw)
    # -----------------------------
    score = (
        confusion_improvement * 50 +
        (coverage_pct / 100) * 30 +
        readability_improvement * 20
    )

    # -----------------------------
    # 🔒 HARD CLAMP (NON-NEGOTIABLE)
    # -----------------------------
    final_score = max(0, min(100, score))

    return {
        "clarity_score": round(final_score, 2),
        "confusion_improvement_pct": round(confusion_improvement * 100, 2),
        "coverage_pct": round(coverage_pct, 2),
        "readability_improvement_pct": round(readability_improvement * 100, 2)
    }
