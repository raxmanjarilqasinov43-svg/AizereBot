import os
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import google.generativeai as genai

# ТОКЕНДЕРДІ RENDER-ДІҢ "ENVIRONMENT" БӨЛІМІНЕН ОҚЫТУ
API_TOKEN = os.getenv('BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_KEY')

# Gemini баптау
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

bot = Bot(token=API_TOKEN) if API_TOKEN else None
dp = Dispatcher()

# Боттың мінезі
BOT_CHARACTER = (
    "Сен 11-Д сыныбының виртуалды оқушысысың. Әкең Ислам — тарихшы, "
    "анаң Хурзия — математик. Жасаушың — Рахман. Қазақша сөйле. "
    "Ақылды әрі қалжыңбас бол. Сыныптастарыңа көмектес."
)

def main_menu():
    buttons = [
        [types.KeyboardButton(text="👥 11-Д алтындары"), types.KeyboardButton(text="⏳ ҰБТ-ға қанша қалды?")],
        [types.KeyboardButton(text="👪 Менің ата-анам"), types.KeyboardButton(text="🤫 Мұғалім келе жатыр!")],
        [types.KeyboardButton(text="📖 Менің тарихым"), types.KeyboardButton(text="📜 Сынып заңы")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        f"Сәлем, сыныптас {message.from_user.first_name}! 🎓\n"
        "Мен дайынмын. Маған кез келген сұрақ қой!",
        reply_markup=main_menu()
    )

@dp.message(F.text == "👥 11-Д алтындары")
async def members(message: types.Message):
    await message.answer("📚 11-Д: Ахмет, Нұртас, Нұрбол, Берік, Нұрлыбек, Арайлым, Нұржанат, Элеонора, Гүлфайруз, Жансұлу")

@dp.message(F.text == "👪 Менің ата-анам")
async def parents(message: types.Message):
    await message.answer("👨‍🏫 **Әкем:** Ислам (Тарихшы)\n👩‍🏫 **Анам:** Хурзия (Математик)")

@dp.message(F.text == "⏳ ҰБТ-ға қанша қалды?")
async def timer(message: types.Message):
    diff = datetime(2026, 6, 1) - datetime.now()
    await message.answer(f"⏳ ҰБТ-ға (1-маусымға) **{diff.days} күн** қалды!")

@dp.message(F.text == "🤫 Мұғалім келе жатыр!")
async def alert(message: types.Message):
    await message.answer("📢 **ШУЛАМАҢДАР! МҰҒАЛІМ КЕЛЕ ЖАТЫР!** 🤫📚")

@dp.message()
async def ai_chat(message: types.Message):
    if not model:
        await message.answer("Қате: Gemini кілті орнатылмаған!")
        return

    await bot.send_chat_action(message.chat.id, "typing")
    try:
        response = model.generate_content(f"{BOT_CHARACTER}\n\nСұрақ: {message.text}")
        await message.answer(response.text)
    except Exception as e:
        await message.answer("Кешір, сыныптас, миым шаршап қалды...")

async def main():
    if bot:
        await dp.start_polling(bot)

if __name__ == "__main__":
   # main.py файлының ең астына, asyncio.run(main()) алдына қой:
from threading import Thread
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Бот жұмыс істеп тұр!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# main функциясының ішінде немесе алдында іске қос:
Thread(target=run_web).start()
 asyncio.run(main())
