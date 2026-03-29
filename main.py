import asyncio
import requests
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Сенің BotFather-ден алған токенің
TOKEN = '8591088414:AAGhXkXuEi9z5ZjegIjp48L5wbTFTdCdTsA'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Суреттегі кесте бойынша мәліметтер
schedules = {
    "Дүйсенбі": "1. Keleshek saati\n2. Kimyo\n3. Algebra\n4. Ana-tili\n5. Informatika",
    "Сейсенбі": "1. Ingliz tili\n2. Algebra\n3. Geometriya\n4. Tarbiya\n5. Isbilermenlik tiykar",
    "Сәрсенбі": "1. O'zbek tili\n2. Algebra\n3. Informatika\n4. Jismoniy madaniyat\n5. J.SH.T\n6. Umumjahon tarixi",
    "Бейсенбі": "1. Ingliz tili\n2. Rus tili\n3. Kimyo\n4. J.SH.T\n5. Qq til (Mamleket til)",
    "Жұма": "1. Fizika\n2. Geometriya\n3. O'zbek tili\n4. Biologiya\n5. Adabiyot\n6. Huquq asoslari",
    "Сенбі": "1. Fizika\n2. Ozbekiston tariyx\n3. Astranomiya\n4. O'zbek tili\n5. Biologiya"
}

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="🗓 Сабақ кестесі"), types.KeyboardButton(text="🌤 Нүкіс ауа райы"))
    builder.row(types.KeyboardButton(text="🏆 Күн үздігі"), types.KeyboardButton(text="😂 Әзіл айт"))
    builder.row(types.KeyboardButton(text="🤫 Мұғалім келе жатыр!"))
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Сәлем! Мен Айзеремін ✨ Сынып көмекшісімін. Не істейміз?", 
        reply_markup=main_menu()
    )

@dp.message(F.text == "🗓 Сабақ кестесі")
async def show_days(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for day in schedules.keys():
        builder.add(types.KeyboardButton(text=day))
    builder.row(types.KeyboardButton(text="⬅ Артқа"))
    await message.answer("Күнді таңдаңыз:", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text.in_(schedules.keys()))
async def send_sched(message: types.Message):
    await message.answer(f"📅 {message.text}:\n\n{schedules[message.text]}")

@dp.message(F.text == "🏆 Күн үздігі")
async def get_winner(message: types.Message):
    students = ["Рахман", "Мерей", "Азамат", "Диана", "Әли", "Айсұлтан", "Гүлім"]
    winner = random.choice(students)
    await message.answer(f"🌟 Бүгінгі күннің жұлдызы: **{winner}**! Құттықтаймыз! 👏")

@dp.message(F.text == "🌤 Нүкіс ауа райы")
async def weather(message: types.Message):
    await message.answer("📍 Нүкіс: Қазір +21°C, күн ашық. Керемет күн! ✨")

@dp.message(F.text == "😂 Әзіл айт")
async def joke(message: types.Message):
    jokes = [
        "— Күнделік қайда?\n— Апай, күнделікті үйде ұмытып кетіппін, бірақ басымды ала келдім!",
        "Мұғалім: — Кім өзін ақымақ санаса, орнынан тұрсын.\nБір оқушы тұрады. Мұғалім: — Сен өзіңді шынымен ақымақ санайсың ба?\nОқушы: — Жоқ, сіздің жалғыз тұрғаныңызға ыңғайсызданып кеттім..."
    ]
    await message.answer(random.choice(jokes))

@dp.message(F.text == "🤫 Мұғалім келе жатыр!")
async def alert(message: types.Message):
    await message.answer("📢 **ШУЛАМАҢДАР! МҰҒАЛІМ КЕЛЕ ЖАТЫР!** 🤫📚")

@dp.message(F.text == "⬅ Артқа")
async def back(message: types.Message):
    await message.answer("Басты мәзір:", reply_markup=main_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
