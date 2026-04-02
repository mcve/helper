import os
from google import genai

# Получаем API ключ напрямую из переменных окружения Railway
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Инициализируем клиента
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
    try:
        # Используем стандартное имя модели gemini-1.5-flash
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\n{text}"
        )
        
        # Проверяем, есть ли текст в ответе
        if response.text:
            return response.text
        else:
            return "🤖 Модель не смогла сгенерировать ответ. Попробуй перефразировать."

    except Exception as e:
        # Обработка лимитов (ошибка 429)
        if "429" in str(e):
            return "⚠️ Лимиты бесплатных запросов исчерпаны. Подожди 1 минуту."
        
        # Обработка ошибки 404 (если модель не найдена)
        elif "404" in str(e):
            return "❌ Ошибка: модель gemini-1.5-flash не найдена. Проверь API ключ."
        
        # Любая другая ошибка
        else:
            return f"🤖 Произошла ошибка: {str(e)}"