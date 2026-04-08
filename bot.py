import os
import asyncio
import smtplib
from email.mime.text import MIMEText

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Переменные окружения
TOKEN = os.getenv("BOT_TOKEN")
EMAIL_FROM = os.getenv("SMTP_USER")
EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню
menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📚 Материалы")],
    [KeyboardButton(text="💬 Обратная связь")],
    [KeyboardButton(text="ℹ️ О нас")]
], resize_keyboard=True)

# Отправка email
def send_email(text, user):
    msg = MIMEText(f"От: {user}\n\n{text}", "plain", "utf-8")
    msg["Subject"] = "Новое сообщение из Telegram бота"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return False

# /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\nВыбери нужный раздел:",
        reply_markup=menu
    )

# Материалы
@dp.message(F.text == "📚 Материалы")
async def materials(message: types.Message):
    await message.answer(
        "📚 Обучающие материалы:\n\n"
        "Здесь будут ссылки на лекции и видеоуроки."
    )

# О нас
@dp.message(F.text == "ℹ️ О нас")
async def about(message: types.Message):
    await message.answer(
        "Этот бот создан для ознакомления с дополнительными "
        "материалами и обратной связи в виде жалоб и предложений. "
        "Все сообщения автоматически отправляются на электронную почту."
    )

# Обратная связь
@dp.message(F.text == "💬 Обратная связь")
async def feedback_prompt(message: types.Message):
    await message.answer("Напиши своё сообщение и я отправлю его:")

# Все остальные сообщения → на почту
@dp.message()
async def forward_to_email(message: types.Message):
    user = f"{message.from_user.full_name} (@{message.from_user.username})"
    ok = send_email(message.text, user)
    if ok:
        await message.answer("✅ Сообщение отправлено!")
    else:
        await message.answer("❌ Ошибка отправки. Попробуй позже.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
