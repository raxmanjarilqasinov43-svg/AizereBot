import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import google.generativeai as genai

# ТОКЕНДЕРДІ ОСЫ ЖЕРГЕ ЖАЗ (Қатесіз қой)
API_TOKEN = 'СЕНІҢ_TELEGRAM_BOT_TOKEN'
GEMINI_API_KEY = 'СЕНІҢ_GEMINI_API_KEY'

# Gemini-ді баптау
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Боттың мінезі
BOT_CHARACTER = (
    "Сен 11-Д сыныбының виртуалды оқушысысың. Сенің әкең Ислам — тарих мұғалімі, "
    "анаң Хурзия — математика мұғалімі. Сені жасаған адамның аты - Рахман. "
    "Қазақ тілінде сөйле. Сыныптастарыңа көмектес."
)

def main_menu():
    buttons = [
        [types.KeyboardButton(text="👥 11-Д алтындары"), types.KeyboardButton(text="📅 Сабақ кестесі")],
        [types.KeyboardButton(text="⏳ ҰБТ-ға қанша қалды?"), types.KeyboardButton(text="👪 Менің ата-анам")],
        [types.KeyboardButton(text="📖 Менің тарихым"), types.KeyboardButton(text="🤫 Мұғалім келе жатыр!")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        f"Сәлем, {message.from_user.first_name}! 🎓 11-Д-ның виртуалды оқушысы дайын.\n"
        "Маған кез келген сұрақ қой, мен Gemini арқылы жауап беремін!",
        reply_markup=main_menu()
    )

@dp.message(F.text == "👥 11-Д алтындары")
async def show_members(message: types.Message):
    text = (
        "📚 **11-Д алтындары:**\n\n"
        "⚽️ Ахмет, Нұртас, Нұрбол, Берік, Нұрлыбек\n"
        "🌸 Арайлым, Нұржанат, Элеонора, Гүлфайруз, Жансұлу"
    )
    await message.answer(text)

@dp.message(F.text == "👪 Менің ата-анам")
async def show_parents(message: types.Message):
    await message.answer("👨‍🏫 **Әкем:** Ислам (Тарих мұғалімі)\n👩‍🏫 **Анам:** Хурзия (Математика мұғалімі)")

@dp.message(F.text == "⏳ ҰБТ-ға қанша қалды?")
async def ent_timer(message: types.Message):
    diff = datetime(2026, 6, 1) - datetime.now()
    await message.answer(f"⏳ ҰБТ-ға (1-маусымға) **{diff.days} күн** қалды!")

@dp.message(F.text == "🤫 Мұғалім келе жатыр!")
async def teacher_alert(message: types.Message):
    await message.answer("📢 **ШУЛАМАҢДАР! МҰҒАЛІМ КЕЛЕ ЖАТЫР!** 🤫📚")

# Басқа сұрақтардың бәріне Gemini жауап береді
@dp.message()
async def chat_with_ai(message: types.Message):
    if message.text in ["📅 Сабақ кестесі", "📖 Менің тарихым"]:
        await message.answer("Бұл бөлімді Рахман жақында толтырады! 😊")
        return

    await bot.send_chat_action(message.chat.id, "typing")
    try:
        response = model.generate_content(f"{BOT_CHARACTER}\n\nСұрақ: {message.text}")
        await message.answer(response.text)
    except Exception:
        await message.answer("Кешір, сыныптас, миым кішкене шаршап қалды...")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
