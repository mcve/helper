import os
from openai import OpenAI
from groq import Groq

# Клиенты
ds_client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_voice(file_path):
    try:
        with open(file_path, "rb") as file:
            # Whisper Large V3 на Groq — это топ скорость
            transcription = groq_client.audio.transcriptions.create(
                file=(file_path, file.read()),
                model="whisper-large-v3",
                response_format="text"
            )
        return transcription
    except Exception as e:
        return f"Ошибка Groq: {str(e)}"

def ask_ai(text):
    try:
        response = ds_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Ты элитный PM-ассистент Артема. 2 работы, e-commerce. Отвечай кратко."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка DeepSeek: {str(e)}"