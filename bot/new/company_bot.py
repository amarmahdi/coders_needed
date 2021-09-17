from aiogram import Dispatcher, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as md
from aiogram.types import ContentType, callback_query
import tg_data
import models

BOT = Bot(token=tg_data.TOKEN)
STORAGE = MemoryStorage()
DP = Dispatcher(bot=BOT, storage=STORAGE)
DBMODEL = models.DataBase()
# DBMODEL.init_users_model()
# DBMODEL.init_company_model()
# DBMODEL.init_job_model()


def uData(message):
    return {
        'id': message.chat.id,
        'username': message.chat.username,
        'first_name': message.chat.first_name,
        'last_name': message.chat.last_name,
        'type': message.chat.type
    }


class Form(StatesGroup):
    company_name = State()
    company_logo = State()
    finish = State()


@DP.message_handler(commands=['start'])
async def start(message):
    data = uData(message)
    DBMODEL.add_user(data['id'], data['username'],
                     data['first_name'], data['last_name'], data['type'], True)
    await BOT.send_message(chat_id=message.chat.id, text=f"Hey {data['first_name']}, \n\nWelcome to CodersNeeded telegram BOT 😊")


# @DP.message_handler(content_types=ContentType.PHOTO)
# async def add_company(message):
#     print(message)
#     data = uData(message)
#     if message.text == 'Add Company':
#         await Form.company_name.set()
#         await message.reply("Enter your company name:")


@DP.message_handler(content_types=['text'])
async def add_company(message, state: FSMContext):
    udata = uData(message)
    if message.text == 'Add Company':
        async with state.proxy as data:
            data['user_id'] = udata['id']
            data['type'] = udata['type']
        await Form.company_name.set()
        await message.reply("Enter your company name:")


@DP.message_handler(state=Form.company_name, content_types=ContentType.PHOTO)
async def add_company_name(message, state: FSMContext):
    async with state.proxy() as data:
        data['company_name'] = message.text

    await Form.next()
    await message.reply("Send us your logo:")


@DP.message_handler(state=Form.company_logo)
async def add_company_logo(message, state: FSMContext):
    async with state.proxy() as data:
        data['company_logo'] = message.text

    await message.reply(f"{data['company_name']}")
    await BOT.send_message(chat_id=message.chat.id, text="Are you certain that you have finished your company information")


@DP.message_handler(state=Form.finish)
async def finish_creating_company(message, state: FSMContext):
    async with state.proxy() as data:
        pass

    await BOT.send_message(chat_id=message.chat.id, text=f"{data['company_name']}\n\n {data['company_logo']} \n\n ")

    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dispatcher=DP, skip_updates=False)
