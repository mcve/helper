import os
import time
from google import genai

# Достаем ключ из переменных Railway
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Инициализируем клиента (новый SDK)
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
Ты мой ассистент.
Контекст: 2 работы PM, ecommerce, мало времени.
Задачи: давать фокус, помогать принимать решения, структурировать мысли.
Отвечай кратко.
"""

def ask_ai(text):
    max_retries = 3  # Максимум 3 попытки
    retry_delay = 10  # Пауза 10 секунд между попытками

    for attempt in range(max_retries):
        try:
            # Используем 2.0-flash из твоего диагностического списка
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=f"{SYSTEM_PROMPT}\n\n{text}"
            )
            
            if response.text:
                return response.text
            return "🤖 Модель вернула пустой ответ."

        except Exception as e:
            error_msg = str(e)
            
            # Если это ошибка лимитов (429) и у нас еще остались попытки
            if "429" in error_msg and attempt < max_retries - 1:
                print(f"Лимит достигнут. Попытка {attempt + 1} из {max_retries}. Жду {retry_delay} сек...")
                time.sleep(retry_delay)
                continue  # Идем на следующую итерацию цикла (повторный запрос)
            
            # Если попытки кончились или ошибка другая
            if "429" in error_msg:
                return "⏳ Все попытки исчерпаны. Google сильно перегружен, попробуй через пару минут."
            
            return f"🤖 Произошла ошибка: {error_msg[:100]}..."

    return "🤖 Что-то пошло не так после всех попыток."