import os
import time
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = "Ты краткий PM-ассистент."

def ask_ai(text):
    try:
        # Используем Lite-версию, у неё лимиты обычно лояльнее
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", 
            contents=f"{SYSTEM_PROMPT}\n\n{text}"
        )
        return response.text

    except Exception as e:
        err = str(e)
        if "429" in err:
            # Если словили лимит — пишем прямо
            return "⏳ Google просит подождать. Лимит бесплатных запросов (RPM) исчерпан. Попробуй через 30-60 секунд."
        return f"🤖 Ошибка: {err[:50]}"