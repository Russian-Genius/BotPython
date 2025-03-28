import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7853106555:AAGmG4SGQzkKvxPnBu0OWMl0m38YTSnBkgE"
API_URL = "http://127.0.0.1:8000"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отправить вебхук"), KeyboardButton(text="Получить вебхуки")]
    ],
    resize_keyboard=True
)



@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я работаю с вебхуками.\nВыбери действие:", reply_markup=kb)


@dp.message_handler(lambda message: message.text == "Отправить вебхук")
async def send_webhook(message: types.Message):
    data = {"event": "tg_message", "payload": f"User {message.from_user.id} sent a webhook"}
    response = requests.post(f"{API_URL}/webhook", json=data)
    await message.answer(f" Вебхук отправлен!\nОтвет сервера: {response.json()}")


@dp.message_handler(lambda message: message.text == "Получить вебхуки")
async def get_webhooks(message: types.Message):
    response = requests.get(f"{API_URL}/webhooks")
    data = response.json()
    if not data:
        await message.answer("Нет сохраненных вебхуков.")
        return

    text = "\n".join([f"🔹 {w['id']}: {w['event']} → {w['payload']}" for w in data[-5:]])
    await message.answer(f"Последние вебхуки:\n{text}")



async def main():
    #dp.startup.register(start)
    #dp.startup.register(send_webhook)
    #dp.startup.register(get_webhooks)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
