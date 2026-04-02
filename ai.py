import os
from google import genai

# Получаем API ключ из переменных окружения Railway
# Убедись, что в панели Railway переменная называется именно GEMINI_API_KEY
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
    if not text:
        return "Я не получил текст для анализа."

    try:
        # Используем стандартную модель 1.5-flash (оптимально для лимитов)
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\n{text}"
        )
        
        if response.text:
            return response.text
        else:
            return "🤖 Хм, не удалось сформулировать ответ. Попробуй еще раз."

    except Exception as e:
        error_msg = str(e)
        
        # Обработка лимитов (429)
        if "429" in error_msg:
            return "⚠️ Лимиты бесплатных запросов исчерпаны. Подожди 1 минуту."
        
        # Обработка заблокированного/неверного ключа (403/400) или модели (404)
        elif "404" in error_msg or "403" in error_msg:
            return "❌ Ошибка авторизации или модели. Проверь, что в Railway установлен НОВЫЙ API Key."
        
        else:
            return f"🤖 Произошла системная ошибка: {error_msg}"