# core/ingestion/loader.py

import pdfplumber

def load_file(file):
    if file.name.endswith(".pdf"):
        return _load_pdf(file)
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise ValueError("Unsupported file type")

def _load_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text
