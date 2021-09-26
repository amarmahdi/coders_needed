import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram import types
from aiogram.types import ContentType
from callbacks import callBackBottons

bot = Bot(token="1931097676:AAHNPkDc57BhRbvHLMfS46QPUtP7zAyKVek")
chId = '-1001191762354'
dp = Dispatcher(bot=bot)
cb = callBackBottons()


class Keyboards:
    def __init__(self) -> None:
        pass

    def keyb(self):
        key = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        phone_button = types.KeyboardButton(
            text="Get Phone", request_contact=True)
        location_button = types.KeyboardButton(
            text="Get Location", request_location=True)
        key.add(phone_button, location_button)
        return key


@dp.message_handler(commands=['start'])
async def poster(message):
    print(message)
    await bot.send_message(chat_id='@TestCodersNeededAdmins', text="hello there", reply_markup=cb.ADbuttons())


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=False)
