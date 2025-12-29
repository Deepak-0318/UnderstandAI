def compute_clarity_score(confusion_delta, coverage_pct, readability_delta):
    """
    Produces final clarity score (1–100)
    """

    confusion_improvement = (
        (confusion_delta["before_confusion"] - confusion_delta["after_confusion"])
        / max(confusion_delta["before_confusion"], 1)
    )

    readability_improvement = (
        (readability_delta["before_grade"] - readability_delta["after_grade"])
        / max(readability_delta["before_grade"], 1)
    )

    score = (
        confusion_improvement * 50 +
        (coverage_pct / 100) * 30 +
        readability_improvement * 20
    )
    final_score = min(score * 100, 95)
    return {
        "clarity_score": round(final_score, 2),
        "confusion_improvement_pct": round(confusion_improvement * 100, 2),
        "coverage_pct": coverage_pct,
        "readability_improvement_pct": round(readability_improvement * 100, 2)
    }
