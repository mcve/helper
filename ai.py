import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# --- ДИАГНОСТИКА ---
print("--- ПРОВЕРКА ДОСТУПНЫХ МОДЕЛЕЙ ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Доступна модель: {m.name}")
except Exception as e:
    print(f"Не удалось получить список моделей: {e}")
print("---------------------------------")

SYSTEM_PROMPT = "Ты PM-ассистент в e-commerce. Отвечай кратко и по делу."

def ask_ai(text):
    try:
        # Пытаемся использовать 1.5-flash. Если упадет — попробуем gemini-pro (1.0)
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\n{text}")
        except:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"{SYSTEM_PROMPT}\n\n{text}")
            
        return response.text
    except Exception as e:
        error_str = str(e)
        if "429" in error_str:
            return "⚠️ Лимиты Google. Подожди минуту."
        return f"🤖 Ошибка API: {error_str[:100]}"