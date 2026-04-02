import os
from google import genai

# Ключ из переменных Railway
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Используем новый SDK, так как старый официально всё
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
Ты мой ассистент.
Контекст: 2 работы PM, ecommerce, мало времени.
Задачи: фокус, решения, структура.
Отвечай кратко.
"""

def ask_ai(text):
    try:
        # Используем модель gemini-2.0-flash, которая есть в твоем списке
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{SYSTEM_PROMPT}\n\n{text}"
        )
        
        if response.text:
            return response.text
        return "🤖 Пустой ответ от модели."

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return "⚠️ Лимиты! Подожди минуту."
        return f"🤖 Ошибка API: {error_msg[:100]}"