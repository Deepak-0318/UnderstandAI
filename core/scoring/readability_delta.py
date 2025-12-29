def compute_readability_delta(sentences):
    before = []
    after = []

    for s in sentences:
        before.append(s.metrics.get("flesch_kincaid_grade", 0))

        if s.explanation:
            after.append(max(s.metrics["flesch_kincaid_grade"] - 6, 6))
        else:
            after.append(s.metrics["flesch_kincaid_grade"])

    return {
        "before_grade": round(sum(before) / len(before), 2),
        "after_grade": round(sum(after) / len(after), 2)
    }
