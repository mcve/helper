import os
from openai import OpenAI

# Инициализируем клиента DeepSeek через протокол OpenAI
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = """
Ты — элитный PM-ассистент. 
Контекст: Артем, 2 работы PM, e-commerce, дропшиппинг. 
Твоя задача: давать четкий фокус, помогать с решениями по SDLC и маркетингу. 
Отвечай максимально кратко, по делу, без "воды".
"""

def ask_ai(text):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            stream=False
        )
        
        if response.choices:
            return response.choices[0].message.content
        return "🤖 DeepSeek прислал пустой ответ."

    except Exception as e:
        err_msg = str(e)
        # Обработка типичных ошибок
        if "balance" in err_msg.lower():
            return "❌ На балансе DeepSeek закончились средства."
        elif "429" in err_msg:
            return "⏳ Лимиты DeepSeek. Попробуй через минуту."
        
        return f"🤖 Ошибка DeepSeek: {err_msg[:100]}"