import base64
import codecs
import json
from telegram.utils import helpers
from telegram.bot import Bot
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler, PicklePersistence

BOT_ID = "-1001355338176"
BOT_TOKEN = "1341348836:AAFf-LQeV1ZByCN9MhOkF7zyaXfQ3AIOdSw"
FIRSTQID = 0
user_id = 0
bot = Bot(token=BOT_TOKEN)
TYPE, DESC, CMP, JOBTYPES, FINAL = range(5)

reply_keyboard = [['Permanent', 'Remote'],
                  ['Contractual']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def filterJobData(jid):
    cur_job = None
    alljobs = json.load(
        open('/home/anonny/scrapers/project_cneeded/data.json'))
    for data in alljobs:
        if jid == data["job_id"]:
            cur_job = data
    return cur_job

# use this from django admin or somewhere to send messages
# and start sync


def messageSender():
    alljobs = json.load(
        open('/home/anonny/scrapers/project_cneeded/data.json'))
    for data in alljobs:
        message = """\nJob Title: {}\n\nCompany: {}\n\nJob Type: {}\n\nDescription: {}""".format(
            data['title'], data['company'], data['jobtype'], data['desc']
        )

        deepURL = helpers.create_deep_linked_url(
            bot.get_me().username, data['job_id'], group=False)
        keyboard = [[InlineKeyboardButton(
            "Apply", callback_data='some_message', url=deepURL)]]

        x = bot.send_message(chat_id=BOT_ID, text=message,
                             reply_markup=InlineKeyboardMarkup(keyboard))
    # return x

    # Handle callback here mane


def callback_query_handler(bot, update):
    if bot.callback_query.data == "suck ma dick":
        print(bot._effective_user.__dict__)
        chat_id = bot._effective_user.id
        print(chat_id)
        bot.sendMessage(
            chat_id=chat_id,
            text='Help text for user ...',
        )


def edit_message():
    message_id = 4
    chat_id = -1001355338176
    bot.editMessageText(
        message_id=message_id,
        chat_id=chat_id,
        text="Message to update")


# reply back based on the input
def use_reply(user_input, mid):
    print(FIRSTQID)
    if FIRSTQID is not None:
        if mid - FIRSTQID == 1:
            return "You have replied to my message"
        else:
            return "input parse error"
    else:
        return "Nigga"


def handle_reply(update, context):
    user_input = update.message.text
    update.message.reply_text(
        use_reply(user_input, int(update.message.message_id)))


def start(update, context):
    data = filterJobData(context.args[0])
    message = """\nJob Title: {}\n\nCompany: {}\n\nJob Type: {}\n\nDescription: {}\n\nTo apply contact: {}""".format(
        data['title'], data['company'], data['jobtype'], data['desc'], "https://t.me/%s" % data['repuname']
    )
    FIRSTQID = int(update.message.message_id)
    update.message.reply_text(message)
    print(FIRSTQID)


def cancel(update, context):
    # del context.user_data
    print("!"*30)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def strt(update, context):
    update.message.reply_text(
        'Enter the product name: ')
    return TYPE


def alldata(update, context):
    print(context)
    print(context.user_data)


def name(update, context):
    user = update.message.from_user
    context.user_data['job_name'] = update.message.text
    update.message.reply_text('Enter the product description here: ',
                              reply_markup=ReplyKeyboardRemove())

    return DESC


def desc(update, context):
    user = update.message.from_user
    context.user_data['job_desc'] = update.message.text
    update.message.reply_text('Enter company name: ')
    return CMP


def job_types(update, context):
    user = update.message.from_user
    context.user_data['company'] = update.message.text
    update.message.reply_text('Enter', reply_markup=markup)
    return JOBTYPES

# TODO save final status here and manage data


def final(update, context):
    text = update.message.text.lower()
    context.user_data['job_type'] = text
    update.message.reply_text(
        "Your Job has been submitted !!")
    return FINAL


# def end_response(update, context):
#     text = update.message.text.lower()
#     context.user_data['job_type'] = text
#     update.message.reply_text("Your Job has been submitted !!")

#     return ConversationHandler.END


def main():
    tst = not False
    if tst:
        pp = PicklePersistence(filename='conversationbot')
        updater = Updater(
            BOT_TOKEN, use_context=True, persistence=pp)
        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(
            CallbackQueryHandler(callback_query_handler))
        updater.dispatcher.add_handler(CommandHandler('add', handle_reply))
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('str', strt)],

            states={
                TYPE: [MessageHandler(Filters.text, name)],

                DESC: [MessageHandler(Filters.text, desc), ],

                CMP: [MessageHandler(Filters.text, job_types)],
                JOBTYPES: [MessageHandler(Filters.regex('^(Remote|Permanent|Contractual)$'), final)],
                # FINAL: [MessageHandler(Filters.text, end_response)]
                # BIO: [MessageHandler(Filters.text & ~Filters.command, bio)]
            },

            fallbacks=[CommandHandler('cancel', cancel)]
        )
        updater.dispatcher.add_handler(CommandHandler('cancel', cancel))
        updater.dispatcher.add_handler(conv_handler)
        updater.dispatcher.add_handler(CommandHandler('alldata', alldata))
        updater.start_polling()
        updater.idle()
    else:
        messageSender()


if __name__ == "__main__":
    main()
