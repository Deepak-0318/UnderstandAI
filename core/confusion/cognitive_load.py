def compute_cognitive_load(sentence):
    """
    Produces a single confusion score per sentence (0–100+)
    """

    score = 0.0
    m = sentence.metrics

    # 1️⃣ Readability (FK Grade)
    fk = m.get("flesch_kincaid_grade", 0)
    if fk > 10:
        score += (fk - 10) * 2.0

    # 2️⃣ Sentence length
    wc = m.get("word_count", 0)
    if wc > 15:
        score += (wc - 15) * 1.5

    # 3️⃣ Passive voice
    if m.get("passive_voice"):
        score += 5.0

    # 4️⃣ Medical jargon density
    jargon_density = m.get("medical_jargon_density", 0)
    score += jargon_density * 20.0

    # 5️⃣ Undefined concepts
    undefined_count = m.get("undefined_concept_count", 0)
    score += undefined_count * 10.0

    sentence.metrics["cognitive_load_score"] = round(score, 2)
    return sentence
