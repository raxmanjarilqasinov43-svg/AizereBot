import asyncio
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import google.generativeai as genai

# ТОКЕНДЕРДІ ОСЫ ЖЕРГЕ ЖАЗ
API_TOKEN = 'СЕНІҢ_TELEGRAM_BOT_TOKEN'
GEMINI_API_KEY = 'СЕНІҢ_API_КІЛТІҢ' # Осы жерге 1000110347.jpg-дағы кілтті қой

# Gemini баптаулары
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Боттың мінезі (Историясы)
BOT_CHARACTER = (
    "Сен 11-Д сыныбының виртуалды оқушысысың. Сенің әкең Ислам — тарих мұғалімі, "
    "анаң Хурзия — математика мұғалімі. Сені жасаған адамның аты - Рахман. "
    "Сен ақылды, кішіпейіл және қалжыңбас баласың. Қазақ тілінде сөйле. "
    "Сыныптастарыңа көмектес, бірақ мұғалімнің баласы екеніңді ұмытпа!"
)

def main_menu():
    buttons = [
        [types.KeyboardButton(text="👥 11-Д алтындары"), types.KeyboardButton(text="📅 Бүгінгі кесте")],
        [types.KeyboardButton(text="⏳ ҰБТ-ға дайындық"), types.KeyboardButton(text="🎭 Көңіл-күй?")],
        [types.KeyboardButton(text="📖 Менің тарихым"), types.KeyboardButton(text="👪 Менің ата-анам")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        f"Сәлем, сыныптас! Мен 11-Д-ның виртуалды оқушысымын. 🎓\n"
        "Маған кез келген сұрақ қойсаң болады, мен Gemini интеллектісімен жауап беремін!",
        reply_markup=main_menu()
    )

@dp.message(F.text == "👪 Менің ата-анам")
async def bot_family(message: types.Message):
    await message.answer("👨‍🏫 Әкем: Ислам (Тарихшы)\n👩‍🏫 Анам: Хурзия (Математик)\n🛠 Жасаушым: Рахман")

@dp.message(F.text == "📖 Менің тарихым")
async def bot_story(message: types.Message):
    await message.answer("Мен мұғалімдер отбасында өскен, Рахман жасаған 11-Д-ның цифрлы оқушысымын! ✨")

# Барлық басқа мәтіндерді Gemini өңдейді
@dp.message()
async def chat_with_ai(message: types.Message):
    # Мәзір батырмалары болса, жауап бермеу үшін
    if message.text in ["👥 11-Д алтындары", "📅 Бүгінгі кесте", "⏳ ҰБТ-ға дайындық", "🎭 Көңіл-күй?", "📖 Менің тарихым", "👪 Менің ата-анам"]:
        if message.text == "⏳ ҰБТ-ға дайындық":
            diff = datetime(2026, 6, 1) - datetime.now()
            await message.answer(f"⏳ ҰБТ-ға {diff.days} күн қалды. Дайындық қалай?")
        elif message.text == "👥 11-Д алтындары":
            await message.answer("📚 11-Д: Ахмет, Нұртас, Нұрбол, Берік, Нұрлыбек, Арайлым, Нұржанат, Элеонора, Гүлфайруз, Жансұлу")
        return

    await bot.send_chat_action(message.chat.id, "typing")
    try:
        prompt = f"{BOT_CHARACTER}\n\nСыныптас: {message.text}"
        response = model.generate_content(prompt)
        await message.answer(response.text)
    except Exception:
        await message.answer("Кешір, сыныптас, миым кішкене шаршап қалды... Кейінірек сұрашы.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
