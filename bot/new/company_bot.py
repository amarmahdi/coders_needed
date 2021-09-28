import asyncio
from aiogram import Dispatcher, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.types import ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types.callback_query import CallbackQuery
import aiogram.utils.markdown as md
from aiogram.types import ContentType, ReplyKeyboardRemove
from callbacks import callBackBottons, CPCallbackData, ADCallbackData, AUCallbackData, JADCallbackData
from KeyBoard import KeyBoards
import tg_data
import models

BOT = Bot(token=tg_data.TOKEN)
STORAGE = MemoryStorage()
DP = Dispatcher(bot=BOT, storage=STORAGE)
DBMODEL = models.DataBase()
KB = KeyBoards()
CB = callBackBottons()
Loop = asyncio.get_event_loop()
DBMODEL.init_users_model()
DBMODEL.init_company_model()
DBMODEL.init_job_model()


def uData(message):
    return {
        'id': message.chat.id,
        'username': message.chat.username,
        'first_name': message.chat.first_name,
        'last_name': message.chat.last_name,
        'type': message.chat.type
    }


messages = {
    'msg_id': None,
    'company_logo': None,
    'company_name': None,
    'company_email': None,
    'company_phone': None,
    'isActive': False
}


jobData = {
    'job_id': None,
    'job_title': None,
    'company_name': None,
    'job_desc': None,
    'job_type': None,
    'category': None,
    'contact_method': None,
}


class Form(StatesGroup):
    UserData = State()
    company_name = State()
    company_email = State()
    company_phone = State()
    company_logo = State()
    last = State()


class PostForm(StatesGroup):
    job_title = State()
    company_name = State()
    job_desc = State()
    job_type = State()
    category = State()
    contact_method = State()
    review = State()


msg1 = "Company Name: {}\nCompany Email: {}\nCompany Phone: {}\n {}"
msg2 = "Company Logo: {}\nCompany Name: {}\nCompany Email: {}\nCompany Phone: {} \n {}"
jobP = "Job Title: {}\nCompany Name: {}\nJob Type: {}\nJob Description: {}\nCategory: {}\nContact Method: {}"


@DP.message_handler(commands=['start'], content_types=['text'])
async def start(message):
    if message.text == '/start' or message.text == 'Back to main menu':
        data = uData(message)
        if DBMODEL.get_user(message.chat.id) != None:
            await BOT.send_message(
                chat_id=message.chat.id,
                text=f"Hey {data['first_name']}, \n\nWelcome back! \n\n",
                reply_markup=KB.main()
            )
        else:
            await BOT.send_message(
                chat_id=message.chat.id,
                text="To start you have to share your contacts",
                reply_markup=KB.getPhone()
            )
            await Form.UserData.set()


@DP.message_handler(state=Form.UserData, content_types=ContentType.CONTACT)
async def getUserData(message, state: FSMContext):
    data = uData(message)
    async with state.proxy() as contactData:
        contactData['userContact'] = message.contact.phone_number
    DBMODEL.add_user(data['id'], data['username'], data['first_name'],
                     data['last_name'], str(contactData['userContact']),
                     data['type'], True)
    await BOT.send_message(
        chat_id=message.chat.id,
        text=f"Hey {data['first_name']}, \n\nWelcome to CodersNeeded telegram BOT 😊 \n\n",
        reply_markup=KB.main()
    )
    await state.finish()


@DP.message_handler(content_types=['text'])
async def job_post_handler(message):
    if message.text == 'Post Job':
        await BOT.send_message(
            chat_id=message.chat.id,
            text="Let's get that title"
        )
        await PostForm.job_title.set()


@ DP.message_handler(state='*', commands='cancel')
@ DP.message_handler(Text(equals='cancel', ignore_case=True))
async def cancel_state(message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await BOT.send_message(
        chat_id=message.chat.id,
        text="Canceled",
        reply_markup=ReplyKeyboardRemove()
    )


@DP.message_handler(content_types=['text'])
async def add_company(message, state: FSMContext):
    udata = uData(message)
    if message.text == 'Add Company':
        async with state.proxy() as data:
            data['user_id'] = udata['id']
            data['type'] = udata['type']
        await BOT.send_message(
            chat_id=message.chat.id,
            text="Add company name: ",
            reply_markup=ReplyKeyboardRemove()
        )
        await Form.company_name.set()


@ DP.message_handler(state=Form.company_name)
async def add_company_name(message, state: FSMContext):
    check = DBMODEL.get_company(message.text)
    if check == None:
        async with state.proxy() as data:
            data['company_name'] = message.text

        await Form.next()
        await BOT.send_message(
            chat_id=message.chat.id,
            text="Enter your company email *Optional",
            reply_markup=KB.skip()
        )
    else:
        await BOT.send_message(
            chat_id=message.chat.id,
            text="The name you provided is taken. Try another name!"
        )


@ DP.message_handler(state=Form.company_email)
async def add_company_email(message, state: FSMContext):
    if message.text == "Previous":
        await BOT.send_message(
            chat_id=message.chat.id,
            text="Change your company name",
            reply_markup=ReplyKeyboardRemove()
        )
        await Form.previous()
    elif message.text != "Skip":
        check = DBMODEL.get_company(message.text)
        if check == None:
            async with state.proxy() as data:
                if message.text != None:
                    data['company_email'] = message.text

            await Form.next()
            await BOT.send_message(
                chat_id=message.chat.id,
                text="Enter Your company Phone"
            )
        else:
            await BOT.send_message(
                chat_id=message.chat.id,
                text="The email you entered is taken. Try another email!"
            )
    elif message.text == "Skip":
        async with state.proxy() as data:
            data['company_email'] = 'None'
        await Form.next()
        await BOT.send_message(
            chat_id=message.chat.id,
            text="Enter Your company Phone",
            reply_markup=ReplyKeyboardRemove()
        )


@ DP.message_handler(state=Form.company_phone)
async def add_company_phone(message, state: FSMContext):
    async with state.proxy() as data:
        data['company_phone'] = message.text

    await Form.next()
    await BOT.send_message(
        chat_id=message.chat.id,
        text="Send Your logo *Optional",
        reply_markup=KB.skip()
    )


@ DP.message_handler(state=Form.company_logo, content_types=[ContentType.PHOTO, 'text'])
async def add_company_logo(message, state: FSMContext):
    if(message.text != 'Skip'):
        async with state.proxy() as data:
            data['company_logo_id'] = message.photo[0].file_id
        await Form.next()
        await BOT.send_message(
            chat_id=message.chat.id,
            text="Check if you miss anything",
            reply_markup=KB.check()
        )
    elif message.text == 'Skip':
        async with state.proxy() as data:
            data['company_logo_id'] = 'None'
        await Form.next()
        await BOT.send_message(
            chat_id=message.chat.id,
            text="Check if you miss anything",
            reply_markup=KB.check()
        )


@ DP.message_handler(state=Form.last)
async def last_check(message, state: FSMContext):
    if message.text == "Check":
        async with state.proxy() as data:
            data['active'] = False
        txt = "\n\nYour Profile is being verified.\nCoders Needed"
        messages['company_logo'] = data['company_logo_id']
        messages['company_name'] = data['company_name']
        messages['company_email'] = data['company_email']
        messages['company_phone'] = data['company_phone']
        messages['isActive'] = data['active']
        messages['type'] = data['type']
        print(message.chat.id)
        if data['company_logo_id'] != 'None':
            await state.finish()
            await BOT.send_photo(
                chat_id=message.chat.id,
                photo=data['company_logo_id'],
                caption=msg1.format(
                    data['company_name'],
                    data['company_email'],
                    data['company_phone'],
                    ''
                ),
                reply_markup=CB.CPbuttons(edit_msg=str(txt))
            )
        else:
            await state.finish()
            await BOT.send_message(
                chat_id=message.chat.id,
                text=msg2.format(
                    data['company_logo_id'],
                    data['company_name'],
                    data['company_email'],
                    data['company_phone'],
                    ''
                ),
                reply_markup=CB.CPbuttons(edit_msg=str(txt))
            )


@ DP.callback_query_handler(CPCallbackData.filter(action='Proceed'))
async def finish_creating_company(query: CallbackQuery, callback_data: dict):
    msg = callback_data['e_message']
    messages['msg_id'] = query.message.message_id
    if messages['company_logo'] != 'None':
        await BOT.edit_message_caption(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            caption=msg1.format(
                messages['company_name'],
                messages['company_email'],
                messages['company_phone'],
                msg
            )
        )
        await BOT.send_photo(
            chat_id="@TestCodersNeededAdmins",
            photo=messages['company_logo'],
            caption=msg1.format(
                messages['company_name'],
                messages['company_email'],
                messages['company_phone'],
                ''
            ),
            reply_markup=CB.ADbuttons('Verified')
        )
    else:
        await BOT.edit_message_text(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            text=msg2.format(
                messages['company_logo'],
                messages['company_name'],
                messages['company_email'],
                messages['company_phone'],
                msg
            )
        )
        await BOT.send_message(
            chat_id="@TestCodersNeededAdmins",
            text=msg2.format(
                messages['company_logo'],
                messages['company_name'],
                messages['company_email'],
                messages['company_phone'],
                ''
            ),
            reply_markup=CB.ADbuttons('Verified')
        )

    return DBMODEL.add_company(
        query.from_user.id,
        query.message.message_id,
        messages['company_name'],
        messages['company_email'],
        messages['company_logo'],
        messages['company_phone'],
        messages['type'],
        messages['isActive']
    )


@ DP.callback_query_handler(ADCallbackData.filter(action='Accept'))
async def accepted_company(query: CallbackQuery, callback_data: dict):
    msg = callback_data['e_msg']
    if messages['company_logo'] != 'None':
        await BOT.edit_message_caption(
            chat_id="@TestCodersNeededAdmins",
            message_id=query.message.message_id,
            caption=msg1.format(
                messages['company_name'],
                messages['company_email'],
                messages['company_phone'],
                'Verified by {}'.format(query.from_user.first_name)
            )
        )
        await BOT.edit_message_caption(
            chat_id=query.from_user.id,
            message_id=messages['msg_id'],
            caption=msg1.format(
                messages['company_name'],
                messages['company_email'],
                messages['company_phone'],
                msg
            )
        )
    else:
        print(query)
        await BOT.edit_message_text(
            chat_id="@TestCodersNeededAdmins",
            message_id=query.message.message_id,
            text=msg2.format(
                messages['company_logo'],
                messages['company_name'],
                messages['company_email'],
                messages['company_phone'],
                'Verified by {}'.format(query.from_user.first_name)
            )
        )
        await BOT.edit_message_text(
            chat_id=query.from_user.id,
            message_id=messages['msg_id'],
            text=msg2.format(
                messages['company_logo'],
                messages['company_name'],
                messages['company_email'],
                messages['company_phone'],
                msg
            )
        )

    await BOT.send_message(
        chat_id=query.from_user.id,
        text="You Have Been Successfuly Signd Up"
    )
    return DBMODEL.update_company(messages['msg_id'], True)


#################################################
# Jop post handler                              #
# Here are the methods for the job post handler #
#                                               #
#################################################


# job title message handler
@DP.message_handler(state=PostForm.job_title)
async def add_job_title(message, state: FSMContext):
    async with state.proxy() as postData:
        postData['id'] = message.chat.id
        postData['job_title'] = message.text
    await BOT.send_message(
        chat_id=message.chat.id,
        text="What's the company ?",
        reply_markup=ReplyKeyboardRemove()
    )
    await PostForm.company_name.set()


# job title message handler
@DP.message_handler(state=PostForm.company_name)
async def add_company_name(message, state: FSMContext):
    async with state.proxy() as postData:
        postData['company_name'] = message.text
    await BOT.send_message(
        chat_id=message.chat.id,
        text="Tell us about the job ?",
    )

    await PostForm.job_desc.set()

# description handler


@DP.message_handler(state=PostForm.job_desc)
async def add_job_desc(message, state: FSMContext):
    async with state.proxy() as postData:
        postData['job_desc'] = message.text
    await BOT.send_message(
        chat_id=message.chat.id,
        text="Choose the job type ?",
        reply_markup=KB.getJobTypes()
    )

    await PostForm.job_type.set()


# Categorize the job
@DP.message_handler(state=PostForm.job_type)
async def add_job_type(message, state: FSMContext):
    async with state.proxy() as postData:
        postData['job_type'] = message.text
    await BOT.send_message(
        chat_id=message.chat.id,
        text="Categorize your job ?",
        reply_markup=KB.getJobCats()
    )
    await PostForm.contact_method.set()

# define the contact method


@DP.message_handler(state=PostForm.contact_method)
async def add_contact_method(message, state: FSMContext):
    async with state.proxy() as postData:
        postData['category'] = message.text

    await BOT.send_message(
        chat_id=message.chat.id,
        text="Select how applicants should contact you ?",
        reply_markup=KB.getContactType()
    )
    await PostForm.review.set()


@DP.message_handler(state=PostForm.review)
async def add_review(message, state: FSMContext):
    async with state.proxy() as postData:
        postData['contact_method'] = message.text

    jobData['job_id'] = postData['id']
    jobData['job_title'] = postData['job_title']
    jobData['company_name'] = postData['company_name']
    jobData['job_desc'] = postData['job_desc']
    jobData['job_type'] = postData['job_type']
    jobData['category'] = postData['category']
    jobData['contact_method'] = postData['contact_method']

    await BOT.send_message(
        chat_id=message.chat.id,
        text=jobP.format(
            jobData['job_title'],
            jobData['company_name'],
            jobData['job_type'],
            jobData['job_desc'],
            jobData['category'],
            jobData['contact_method']
        ),
        reply_markup=CB.ApproveUpload()
    )
    await state.finish()


@DP.callback_query_handler(AUCallbackData.filter(action='Save'))
async def finish_creating_company(query: CallbackQuery, callback_data: dict):
    await BOT.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text=jobP.format(
            jobData['job_title'],
            jobData['company_name'],
            jobData['job_type'],
            jobData['job_desc'],
            jobData['category'],
            jobData['contact_method']
        ) + "\n\n Your post is sent for moderation, we will get pack you shortly! \n\n Coders Needed"
    )

    await BOT.send_message(
        chat_id="@TestCodersNeededAdmins",
        text=jobP.format(
            jobData['job_title'],
            jobData['company_name'],
            jobData['job_type'],
            jobData['job_desc'],
            jobData['category'],
            jobData['contact_method']
        ),
        reply_markup=CB.JADbuttons()
    )


@DP.callback_query_handler(JADCallbackData.filter(action='Accept'))
async def job_post_accept(query: CallbackQuery, callback_data: dict):
    print(jobData)
    await BOT.send_message(
        chat_id=jobData['job_id'],
        text='You have been verified'
    )


@DP.callback_query_handler(CPCallbackData.filter(action='Cancel'))
async def cancel_createing_company(query: CallbackQuery, callback_data: dict):
    msg = callback_data['e_message']
    if messages['company_logo'] != 'None':
        await BOT.edit_message_caption(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            photo=messages['company_logo'],
            caption=msg1.format(
                messages['company_name'],
                messages['company_email'],
                messages['company_phone'],
                msg
            )
        )
        await BOT.send_message(
            chat_id=query.from_user.id,
            text="Cancel"
        )
    else:
        await BOT.edit_message_text(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            text=msg2.format(
                messages['company_logo'],
                messages['company_name'],
                messages['company_email'],
                messages['company_phone'],
                msg
            )
        )
        await BOT.send_message(
            chat_id=query.from_user.id,
            text="Cancel"
        )


if __name__ == "__main__":
    executor.start_polling(dispatcher=DP, loop=Loop, skip_updates=False)
