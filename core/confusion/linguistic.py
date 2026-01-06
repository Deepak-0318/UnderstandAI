import spacy

nlp = spacy.load("en_core_web_sm")

def compute_linguistic_features(sentence):
    text = sentence.text
    doc = nlp(text)

    words = [token for token in doc if token.is_alpha]

    # 1️⃣ Sentence length
    sentence.metrics["word_count"] = len(words)

    # 2️⃣ Average word length
    if words:
        sentence.metrics["avg_word_length"] = sum(len(w.text) for w in words) / len(words)
    else:
        sentence.metrics["avg_word_length"] = 0

    # 3️⃣ Passive voice detection (simple heuristic)
    sentence.metrics["passive_voice"] = any(
        token.dep_ == "auxpass" for token in doc
    )

    # 4️⃣ Noun phrase count
    sentence.metrics["noun_phrase_count"] = len(list(doc.noun_chunks))

    return sentence
