import os
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import google.generativeai as genai
from threading import Thread
from flask import Flask

# 1. RENDER ҮШІН КІШКЕНТАЙ ВЕБ-СЕРВЕР (ПОРТ ҚАТЕСІН ЖОЮ ҮШІН)
app = Flask('')

@app.route('/')
def home():
    return "Бот жұмыс істеп тұр!"

def run_web():
    # Render беретін портты қолдану немесе 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. БОТТЫҢ НЕГІЗГІ КОДЫ
API_TOKEN = os.getenv('BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_KEY')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

bot = Bot(token=API_TOKEN) if API_TOKEN else None
dp = Dispatcher()

BOT_CHARACTER = "Сен 11-Д сыныбының виртуалды оқушысысың. Жасаушың — Рахман. Қазақша сөйле."

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(f"Сәлем, {message.from_user.first_name}! Мен дайынмын.")

@dp.message()
async def ai_chat(message: types.Message):
    if not model:
        await message.answer("Кілт орнатылмаған.")
        return
    await bot.send_chat_action(message.chat.id, "typing")
    try:
        response = model.generate_content(f"{BOT_CHARACTER}\n\nСұрақ: {message.text}")
        await message.answer(response.text)
    except:
        await message.answer("Кешір, миым шаршап қалды...")

async def main():
    if bot:
        await dp.start_polling(bot)

if __name__ == "__main__":
    # Веб-серверді бөлек ағында іске қосамыз
    Thread(target=run_web).start()
    # Ботты іске қосамыз
    asyncio.run(main())
