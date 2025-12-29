def compute_prerequisite_coverage(sentences):
    total_missing = 0
    covered = 0

    for s in sentences:
        missing = s.metrics.get("undefined_concept_count", 0)
        total_missing += missing

        if s.explanation and missing > 0:
            covered += missing

    coverage_ratio = covered / total_missing if total_missing else 1.0

    return round(coverage_ratio * 100, 2)
