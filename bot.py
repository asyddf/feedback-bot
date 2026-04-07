import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import smtplib
from email.mime.text import MIMEText

# Берём данные из переменных окружения (чтобы не хранить пароли в коде)
TOKEN = os.getenv("TOKEN")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def send_email(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = EMAIL

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)
    server.quit()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Напиши сообщение, и оно придёт на почту. Для материалов введи /content")

@dp.message_handler(commands=['content'])
async def content(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton("Статья 1", url="https://link_to_article"))
    keyboard.add(types.InlineKeyboardButton("Видео урок", url="https://youtube.com/..."))
    await message.reply("Выбирай материал:", reply_markup=keyboard)

@dp.message_handler()
async def forward_to_email(message: types.Message):
    send_email("Сообщение от пользователя", message.text)
    await message.reply("Сообщение отправлено!")

if __name__ == "__main__":
    executor.start_polling(dp)