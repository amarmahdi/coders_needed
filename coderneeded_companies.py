# CODERS NEEDED COMPANY BOT
import base64
import codecs
import json
from telegram.utils import helpers
from telegram.bot import Bot, Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import MessageHandler, Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler, PicklePersistence, CallbackContext
from constants import about_message

# channel bot id
BOT_ID = "-1001355338176"
# company bot id
BOT_TOKEN = "1346826306:AAEBRd8TbKAl4t52gqZGginATw91dTWea38"
bot = Bot(token=BOT_TOKEN)
TYPE, DESC, CMP, JOBTYPES, FINAL = range(5)

reply_keyboard = [['Permanent', 'Remote'],
                  ['Contractual', 'Hourly']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
kb = [[
    KeyboardButton('📝 Add new job'),
    KeyboardButton('🧳 Your Job offers'),
    KeyboardButton('⚙️ Settings')],
    [KeyboardButton('📊 Check Statics')]]
kb_markup = ReplyKeyboardMarkup(kb, resize_keyboard=True)


def callback_query_handler(update: Update, context: CallbackContext):
    if update.callback_query.data == "Submit":
        try:
            query = update.callback_query
            context.bot.answer_callback_query(
                callback_query_id=query.id, text="Your Job post is being verified by Admins Please wait ....",
                show_alert=True
            )
            query.answer()
            query.edit_message_text(
                text="Your job application has been sent for verification",
                show_alert=True
            )
            usr = update._effective_user
            userDetails = {
                'user_id': usr['id'], 'first_name': usr['first_name'],
                'is_bot': usr['is_bot'], 'last_name': usr['last_name'],
                'username': usr['username']}
            finalJobData = context.user_data['user_details'] = userDetails
            print(context.user_data)
        except Exception as e:
            print(e)

    elif update.callback_query.data == "close_application":
        try:
            data = context.user_data
            message = """!!!!!!!! CLOSED !!!!!!!!!!\n\n{}\n\n!!!!!!!! CLOSED !!!!!!!!!!""".format(
                update.callback_query.message.text
            )
            update.callback_query.edit_message_text(
                text=message)
        except Exception as p:
            print(p)

        return ConversationHandler.END


def start(update, context):
    update.message.reply_text(about_message, reply_markup=kb_markup)


def findOpened():
    openedOnes = []
    alljobs = json.load(
        open('/home/anonny/scrapers/coders_needed/data.json'))
    for data in alljobs:
        if data['opened'] == True:
            openedOnes.append(data)
    return openedOnes


def handleMessages(update, context):
    command = update.message.text
    if command == "📝 Add new job":
        update.message.reply_text('Use /cancel to stop posting !')

        keyboard = [[KeyboardButton("Cancel ")],
                    ]
        update.message.reply_text(
            'What is the job\'s Title ? : ')
        return DESC

    elif command == "🧳 Your Job offers":
        # alljobs = json.load(
        #     open('/home/anonny/scrapers/coders_needed/data.json'))
        # for data in alljobs:
        #     message = """\nJob Title: {}\n\nCompany: {}\n\nJob Type: {}\n\nDescription: {}""".format(
        #         data['title'], data['company'], data['jobtype'], data['desc']
        #     )
        # kb = [[
        #     KeyboardButton('📝 Add new job'),
        #     KeyboardButton('🧳 Your Job offers'),
        #     KeyboardButton('⚙️ Settings')],
        #     [KeyboardButton('📊 Check Statics')]]

        keyboard = [[KeyboardButton("Opened")],
                    [InlineKeyboardButton("Closed")],
                    [InlineKeyboardButton("Back To Menu")],
                    ]
        offer_markup = ReplyKeyboardMarkup(keyboard)

        update.message.reply_text(
            "select an option", reply_markup=offer_markup)
        return ConversationHandler.END
    elif command == "Back To Menu":
        update.message.reply_text(
            "select an option", reply_markup=kb_markup)
        return ConversationHandler.END
    elif command == "Opened":
        for data in findOpened():
            # TODO: send this to the server and set it closed **** data['id'] ****
            message = """\nJob Title: {}\n\nCompany: {}\n\nJob Type: {}\n\nDescription: {}""".format(
                data['title'], data['company'], data['jobtype'], data['desc']
            )
            key = [[InlineKeyboardButton(
                "Close application", callback_data='close_application')]]
            update.message.reply_text(
                message, reply_markup=InlineKeyboardMarkup(key))

        return ConversationHandler.END
    elif command == "Closed":
        update.message.reply_text(
            "select an option", reply_markup=kb_markup)
        return ConversationHandler.END

# cancel this shit


def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:")

    user_data.clear()
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
    # update.message.reply_text(about_message, reply_markup=kb_markup)
    return ConversationHandler.END


def strt(update, context):
    update.message.reply_text(
        'What is the job\'s Title ? : ', reply_markup=kb_markup)
    return DESC


def name(update, context):
    user = update.message.from_user
    context.user_data['job_name'] = update.message.text
    update.message.reply_text(
        'Enter the job description here: ')

    return DESC


def desc(update, context):
    user = update.message.from_user
    context.user_data['job_desc'] = update.message.text
    update.message.reply_text(
        'Enter company name: ', reply_markup=ReplyKeyboardRemove(), is_closed=True)
    return CMP


def job_types(update, context):
    user = update.message.from_user
    context.user_data['company'] = update.message.text
    update.message.reply_text('Enter job type: ', reply_markup=markup)
    return JOBTYPES

# TODO save final status here and manage data


def final(update, context):
    data = context.user_data
    text = update.message.text.lower()
    context.user_data['job_type'] = text

    message = """\nJob Title: {}\n\nCompany: {}\n\nJob Type: {}\n\nDescription: {}""".format(
        data['job_name'], data['company'], data['job_type'], data['job_desc']
    )

    keyboard = [[InlineKeyboardButton("✅  Submit", callback_data='Submit')],
                [InlineKeyboardButton("❌  Cancel", callback_data='cancel')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)
    try:
        update.message.reply_text("verify your offer", reply_markup=kb_markup)
    except Exception as e:
        print(e)
    return FINAL


def main():
    pp = PicklePersistence(filename='conversationbot')
    updater = Updater(
        BOT_TOKEN, use_context=True, persistence=pp)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(callback_query_handler))
    # conversation handler starts here man
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('postjob', strt)],

        states={
            TYPE: [MessageHandler(Filters.text, name)],

            DESC: [MessageHandler(Filters.text, desc), ],

            CMP: [MessageHandler(Filters.text, job_types)],
            JOBTYPES: [MessageHandler(Filters.regex('^(Remote|Permanent|Contractual|Hourly)$'), final)],
            # FINAL: [MessageHandler(Filters.text, end_response)]
            # BIO: [MessageHandler(Filters.text & ~Filters.command, bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    updater.dispatcher.add_handler(CommandHandler('cancel', cancel))
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, handleMessages))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
