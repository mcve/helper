import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command # Добавили фильтр команд

from ai import ask_ai
# Пока закомментируй voice, если файл еще не готов, чтобы не было ошибок
# from voice import transcribe 

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# 🚀 Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой PM-ассистент. Присылай мысли — я помогу их структурировать.")

# 📩 Обработка любого текстового сообщения
@dp.message()
async def handle_text(message: types.Message):
    if message.text:
        # Показываем, что бот "печатает", чтобы ожидание не пугало
        await bot.send_chat_action(message.chat.id, "typing")
        
        answer = ask_ai(message.text)
        await message.answer(answer)

# 🎤 Обработка голоса (убедись, что voice.py работает корректно)
@dp.message(lambda message: message.voice)
async def handle_voice(message: types.Message):
    await message.answer("Секунду, слушаю твое сообщение...")
    # Здесь твоя логика скачивания и транскрибации
    # ...

async def main():
    print("Бот запущен и готов к работе!") # Увидишь это в логах Railway
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())