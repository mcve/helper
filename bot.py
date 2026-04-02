import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from ai import ask_ai, transcribe_voice # Импортируем обе функции

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# 🚀 Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, Артем! Я на связи. Присылай текст или ГС — разберем задачи по PM или e-commerce.")

# 🎤 Обработка голосовых сообщений (ГС)
@dp.message(F.voice)
async def handle_voice(message: types.Message):
    await bot.send_chat_action(message.chat.id, "record_voice")
    
    # 1. Скачиваем файл из Telegram
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_on_disk = f"{file_id}.ogg"
    await bot.download_file(file.file_path, file_on_disk)

    # 2. Расшифровываем голос в текст через Groq
    text_from_voice = transcribe_voice(file_on_disk)
    
    # Удаляем временный файл сразу после расшифровки
    if os.path.exists(file_on_disk):
        os.remove(file_on_disk)

    if not text_from_voice or "Ошибка" in text_from_voice:
        await message.answer(f"❌ Не удалось распознать голос: {text_from_voice}")
        return

    # 3. Отправляем полученный текст в DeepSeek
    await bot.send_chat_action(message.chat.id, "typing")
    answer = ask_ai(text_from_voice)
    
    # Отвечаем пользователю, показывая, что мы услышали
    await message.answer(f"🎤 _Вы сказали:_ {text_from_voice}\n\n🤖 {answer}", parse_mode="Markdown")

# 📩 Обработка текстовых сообщений
@dp.message(F.text)
async def handle_text(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    answer = ask_ai(message.text)
    await message.answer(answer)

async def main():
    print("Бот запущен и готов слушать ГС!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())