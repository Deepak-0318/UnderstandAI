import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-flash-latest"

SYSTEM_PROMPT = """
You are a medical explanation assistant.
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
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_PROMPT
    )

    user_prompt = f"""
Original sentence:
"{payload['original_sentence']}"

Missing concepts:
{", ".join(payload['missing_concepts'])}

Explain in 4 steps:
1. What the missing concept means (simple)
2. Everyday analogy
3. Why it matters in this sentence
4. Re-explain the original sentence clearly
"""

    response = model.generate_content(user_prompt)

    return {
        "sentence_id": payload["sentence_id"],
        "explanation": response.text.strip()
    }
