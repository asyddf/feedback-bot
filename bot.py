import os
import smtplib
from email.mime.text import MIMEText

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Переменные окружения
TOKEN = os.getenv("TOKEN")

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Функция отправки email
def send_email(message_text):
    msg = MIMEText(message_text)
    msg['Subject'] = "Новое сообщение из Telegram бота"
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("Ошибка отправки почты:", e)


# Команда старт
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(
        "Привет! 👋\n\n"
        "Напиши сообщение — оно придёт на почту.\n"
        "Для материалов введи /content"
    )

# Раздел с материалами
@dp.message_handler(commands=['content'])
async def content(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton("📄 Статья", url="https://example.com"))
    keyboard.add(types.InlineKeyboardButton("🎥 Видео", url="https://youtube.com"))

    await message.reply("Выбирай материал:", reply_markup=keyboard)

# Все сообщения → на почту
@dp.message_handler()
async def forward_to_email(message: types.Message):
    send_email(message.text)
    await message.reply("Сообщение отправлено ✅")


if __name__ == "__main__":
    executor.start_polling(dp)
