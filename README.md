# Understand AI – Medical Consent Understanding Engine

We don’t just inform patients. We prove understanding happened.

## Problem
Medical consent documents are complex. Patients often sign without fully understanding risks, terms, or implications.

## Solution
Understand AI proactively detects confusing sentences in medical consent documents, explains missing concepts in simple language, and verifies understanding using a measurable Clarity Score.

## Features
- PDF upload (medical consent forms)
- Sentence-level confusion detection (spaCy + textstat)
- Medical jargon & prerequisite detection
- Gemini-powered step-by-step explanations
- Safety & hallucination guard
- Clarity Score (1–100)

## Tech Stack
- UI: Streamlit
- NLP: spaCy, textstat
- LLM: Google Gemini
- PDF Parsing: pdfplumber

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
