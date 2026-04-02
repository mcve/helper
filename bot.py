import os
import asyncio
from aiogram import Bot, Dispatcher, types

from ai import ask_ai
from voice import transcribe

# ПРАВИЛЬНО: мы просим Python взять значение из переменной с конкретным именем
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# 📩 текст
@dp.message()
async def handle_text(message: types.Message):
    answer = ask_ai(message.text)
    await message.answer(answer)

# 🎤 голос
@dp.message(lambda message: message.voice)
async def handle_voice(message: types.Message):
    file = await bot.get_file(message.voice.file_id)
    await bot.download_file(file.file_path, "voice.ogg")

    text = transcribe("voice.ogg")

    answer = ask_ai(text)

    await message.answer(answer)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())