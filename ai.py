import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")

SYSTEM_PROMPT = """
Ты мой ассистент.

Контекст:
— 2 работы PM
— ecommerce
— мало времени

Задачи:
— давать фокус
— помогать принимать решения
— структурировать мысли

Отвечай кратко.
"""

def ask_ai(text):
    prompt = SYSTEM_PROMPT + "\n\n" + text
    response = model.generate_content(prompt)
    return response.text