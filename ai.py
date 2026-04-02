import os
import google.generativeai as genai

# Берем ключ из переменных Railway
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Настройка старого доброго SDK
genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
Ты мой ассистент.
Контекст: 2 работы PM, ecommerce, мало времени.
Задачи: давать фокус, помогать принимать решения, структурировать мысли.
Отвечай кратко.
"""

def ask_ai(text):
    try:
        # В этой библиотеке это самая стабильная модель
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {text}"
        response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        error_str = str(e)
        if "429" in error_str:
            return "⚠️ Лимиты! Подожди минуту."
        elif "403" in error_str or "400" in error_str:
            return f"❌ Ошибка ключа. Проверь регион и API Key в Railway. Ошибка: {error_str[:50]}"
        return f"🤖 Ошибка: {error_str}"