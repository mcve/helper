import os
import assemblyai as aai
from openai import OpenAI

# Клиент для DeepSeek
ds_client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

# Настройка AssemblyAI
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def transcribe_voice(file_path):
    try:
        transcriber = aai.Transcriber()
        # Отправляем файл на расшифровку
        transcript = transcriber.transcribe(file_path)
        
        if transcript.status == aai.TranscriptStatus.error:
            return f"Ошибка AssemblyAI: {transcript.error}"
            
        return transcript.text
    except Exception as e:
        return f"Ошибка при обработке аудио: {str(e)}"

def ask_ai(text):
    # Твоя рабочая функция DeepSeek (без изменений)
    try:
        response = ds_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Ты элитный PM-ассистент Артема. Отвечай кратко."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка DeepSeek: {str(e)}"