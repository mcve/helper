import os
from google import genai
# Если GEMINI_API_KEY прописан в переменных Railway, 
# лучше брать его напрямую через os.getenv, чтобы не зависеть от config.py
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
Ты мой ассистент.
Контекст: 2 работы PM, ecommerce, мало времени.
Задачи: давать фокус, помогать принимать решения, структурировать мысли.
Отвечай кратко.
"""

def ask_ai(text):
    try:
        # Пробуем модель с суффиксом -latest, это самый стабильный вариант для v1beta
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest", 
            contents=f"{SYSTEM_PROMPT}\n\n{text}"
        )
        return response.text
    except Exception as e:
        # Если это ошибка лимитов (429)
        if "429" in str(e):
            return "⚠️ У меня закончились бесплатные запросы к Google. Подожди минуту и попробуй снова."
        # Если модель всё еще не найдена (404)
        elif "404" in str(e):
            return "❌ Ошибка: модель не найдена. Попробуй изменить имя модели в коде на 'gemini-1.5-flash'."
        else:
            return f"🤖 Произошла ошибка: {str(e)}"