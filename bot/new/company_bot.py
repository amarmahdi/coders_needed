from aiogram import Dispatcher, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as md
from aiogram.types import ContentType, ReplyKeyboardRemove
from KeyBoard import KeyBoards
import tg_data
import models

BOT = Bot(token=tg_data.TOKEN)
STORAGE = MemoryStorage()
DP = Dispatcher(bot=BOT, storage=STORAGE)
DBMODEL = models.DataBase()
KB = KeyBoards()
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


@DP.message_handler(commands=['start'], content_types=['text'])
async def start(message):
    if message.text == '/start' or message.text == 'Back to main menu':
        data = uData(message)
        DBMODEL.add_user(data['id'], data['username'],
                         data['first_name'], data['last_name'], data['type'], True)
        await BOT.send_message(chat_id=message.chat.id, text=f"Hey {data['first_name']}, \n\nWelcome to CodersNeeded telegram BOT 😊 \n\n", reply_markup=KB.main())


@DP.message_handler(content_types=['text'])
async def add_company(message, state: FSMContext):
    udata = uData(message)
    if message.text == 'Add Company':
        async with state.proxy() as data:
            data['user_id'] = udata['id']
            data['type'] = udata['type']
        await Form.company_name.set()
        await BOT.send_message(chat_id=message.chat.id, text="Add company name: ", reply_markup=ReplyKeyboardRemove())


@DP.message_handler(state=Form.company_name)
async def add_company_name(message, state: FSMContext):
    async with state.proxy() as data:
        data['company_name'] = message.text

    await Form.next()
    await BOT.send_message(chat_id=message.chat.id, text="Send us your logo:")


@DP.message_handler(state=Form.company_logo, content_types=ContentType.PHOTO)
async def add_company_logo(message, state: FSMContext):
    async with state.proxy() as data:
        data['company_logo_id'] = message.photo[0].file_id
    await message.reply(f"{data['company_name']}")
    await Form.next()
    await BOT.send_message(chat_id=message.chat.id, text="Are you certain that you have finished your company information", reply_markup=KB.finish())


@DP.message_handler(state=Form.finish)
async def finish_creating_company(message, state: FSMContext):
    if message.text == "Finish":
        async with state.proxy() as data:
            pass

        await BOT.send_photo(chat_id=message.chat.id, photo=data['company_logo_id'], caption=f"Company Name: {data['company_name']} \n", reply_markup=ReplyKeyboardRemove())

        await state.finish()


if __name__ == "__main__":
    executor.start_polling(dispatcher=DP, skip_updates=False)
