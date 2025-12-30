# core/ingestion/text_cleaner.py

import re

def clean_text(text: str) -> str:
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def fix_line_wrapping(text: str) -> str:
    """
    Joins lines that were broken due to PDF line wrapping.
    """
    lines = text.split("\n")
    fixed = []

    buffer = ""

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if buffer:
                fixed.append(buffer.strip())
                buffer = ""
            continue

        # If line does NOT end with sentence punctuation, it's likely wrapped
        if not stripped.endswith((".", "!", "?")):
            buffer += stripped + " "
        else:
            buffer += stripped
            fixed.append(buffer.strip())
            buffer = ""

    if buffer:
        fixed.append(buffer.strip())

    return "\n".join(fixed)
