import textstat

def compute_readability(sentence):
    """
    Adds readability metrics to sentence.metrics
    """
    text = sentence.text

    sentence.metrics["flesch_reading_ease"] = textstat.flesch_reading_ease(text)
    sentence.metrics["flesch_kincaid_grade"] = textstat.flesch_kincaid_grade(text)

    return sentence
