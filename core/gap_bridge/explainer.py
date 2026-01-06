import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-flash-latest"

SYSTEM_PROMPT = """
You are a medical explanation assistant.
<<<<<<< HEAD

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

=======
Your job is to explain medical consent text clearly WITHOUT adding new medical facts.

STRICT RULES:
- Do NOT add new risks, treatments, or statistics
- Do NOT give medical advice
- Do NOT change meaning
- Only explain concepts already present
- Use simple language
- Use analogies where helpful
"""

def generate_explanation(payload: dict):
>>>>>>> 8b2bf7a6986c92aa80b463f444ef03fa34b79693
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_PROMPT
    )

    user_prompt = f"""
<<<<<<< HEAD
Medical sentence:
\"\"\"{payload['original_sentence']}\"\"\"

Confusing or missing concepts:
{", ".join(payload.get("missing_concepts", []))}

Explain this sentence in plain English for a patient.
=======
Original sentence:
"{payload['original_sentence']}"

Missing concepts:
{", ".join(payload['missing_concepts'])}

Explain in 4 steps:
1. What the missing concept means (simple)
2. Everyday analogy
3. Why it matters in this sentence
4. Re-explain the original sentence clearly
>>>>>>> 8b2bf7a6986c92aa80b463f444ef03fa34b79693
"""

    response = model.generate_content(user_prompt)

<<<<<<< HEAD
    # 🔒 HARD GUARANTEE: always return clean text
    if hasattr(response, "text") and response.text:
        return response.text.strip()

    raise ValueError("Gemini returned empty explanation")
=======
    return {
        "sentence_id": payload["sentence_id"],
        "explanation": response.text.strip()
    }
>>>>>>> 8b2bf7a6986c92aa80b463f444ef03fa34b79693
