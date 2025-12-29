def classify_confusion(sentence):
    score = sentence.metrics.get("cognitive_load_score", 0)

    if score < 15:
        label = "CLEAR"        # 🟩
    elif score < 35:
        label = "MEDIUM"       # 🟨
    else:
        label = "HIGH"         # 🟥

    sentence.confusion_label = label
    return sentence
