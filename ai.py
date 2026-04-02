import os
from google import genai
from config import GEMINI_API_KEY

# Инициализируем клиента по новому стандарту
client = genai.Client(api_key=GEMINI_API_KEY)

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
    # Используем новую модель gemini-2.0-flash (она быстрее и умнее старой pro)
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\n{text}"
    )
    return response.text