import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-flash-latest"

SYSTEM_PROMPT = """
You are a medical explanation assistant.

Your task is to help a patient understand medical consent language.

STRICT RULES:
- Do NOT add new medical facts
- Do NOT give medical advice
- Do NOT change the meaning
- Do NOT rewrite the sentence
- Explain only what is already implied
- Use simple, non-technical language
- Output ONE short paragraph (3–4 sentences max)
- NO bullet points, NO numbering, NO markdown
"""

def generate_explanation(payload: dict) -> str:
    """
    Returns a plain-text explanation string.
    MUST NOT return dicts or structured data.
    """

    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_PROMPT
    )

    user_prompt = f"""
Medical sentence:
\"\"\"{payload['original_sentence']}\"\"\"

Confusing or missing concepts:
{", ".join(payload.get("missing_concepts", []))}

Explain this sentence in plain English for a patient.
"""

    response = model.generate_content(user_prompt)

    # 🔒 HARD GUARANTEE: always return clean text
    if hasattr(response, "text") and response.text:
        return response.text.strip()

    raise ValueError("Gemini returned empty explanation")
