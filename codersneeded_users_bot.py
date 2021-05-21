import base64
import codecs
import json
from telegram.utils import helpers
from telegram.bot import Bot, Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import MessageHandler, Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler, PicklePersistence, CallbackContext

BOT_ID = "CNEED_BOT_ID"
BOT_TOKEN = "CNEEDS_BOT_TOKEN"
FIRSTQID = 0
user_id = 0
bot = Bot(token=BOT_TOKEN)
TYPE, DESC, CMP, JOBTYPES, FINAL = range(5)

reply_keyboard = [['Permanent', 'Remote'],
                  ['Contractual', 'Hourly']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def filterJobData(jid):
    cur_job = None
    alljobs = json.load(
        open('/home/anonny/scrapers/coders_needed/data.json'))
    for data in alljobs:
        if jid == data["job_id"]:
            cur_job = data
    return cur_job

# use this from django admin or somewhere to send messages
# and start sync


def messageSender():
    alljobs = json.load(
        open('/home/anonny/scrapers/coders_needed/data.json'))
    for data in alljobs:
        message = """\nJob Title: {}\n\nCompany: {}\n\nJob Type: {}\n\nDescription: {}""".format(
            data['title'], data['company'], data['jobtype'], data['desc']
        )

        deepURL = helpers.create_deep_linked_url(
            bot.get_me().username, data['job_id'], group=False)
        keyboard = [[InlineKeyboardButton(
            "Apply", callback_data='some_message', url=deepURL),
            InlineKeyboardButton(
            "Share", callback_data='share_applicatoin', url='https://t.me/share/url?url='+message)]]

        x = bot.send_message(chat_id=BOT_ID, text=message,
                             reply_markup=InlineKeyboardMarkup(keyboard))
    # return x

    # Handle callback here mane


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

    return ConversationHandler.END


def edit_message():
    message_id = 4
    chat_id = -1001355338176
    bot.editMessageText(
        message_id=message_id,
        chat_id=chat_id,
        text="Message to update")


# reply back based on the input
def use_reply(user_input, mid):
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
    if len(context.args) > 0:
        # TODO filter a job with this id
        data = filterJobData(context.args[0])
        print(data)
        message = """\nJob Title: {}\n\nCompany: {}\n\nJob Type: {}\n\nDescription: {}\n\nTo apply contact: {}""".format(
            data['title'], data['company'], data['jobtype'], data['desc'], "https://t.me/%s" % data['repuname']
        )
        update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    else:
        # FIRSTQID = int(update.message.message_id)
        update.message.reply_text("Hello there welcome to coders needed bot !\nUse these commands to manage your applications",
                                  reply_markup=ReplyKeyboardRemove())
    # print(FIRSTQID)


def cancel(update, context):
    # del context.user_data
    print("!"*30)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def strt(update, context):
    update.message.reply_text(
        'What is the job\'s Title ? : ')
    return TYPE


# def alldata(update, context):
#     print(context)
#     print(context.user_data)


def name(update, context):
    user = update.message.from_user
    context.user_data['job_name'] = update.message.text
    update.message.reply_text('Enter the job description here: ',
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
    data = context.user_data
    text = update.message.text.lower()
    context.user_data['job_type'] = text

    message = """\nJob Title: {}\n\nCompany: {}\n\nJob Type: {}\n\nDescription: {}""".format(
        data['job_name'], data['company'], data['job_type'], data['job_desc']
    )

    keyboard = [[InlineKeyboardButton("✅  Submit", callback_data='Submit')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message,
                              reply_markup=reply_markup
                              )

    return FINAL


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
            entry_points=[CommandHandler('postjob', strt)],

            states={
                TYPE: [MessageHandler(Filters.text, name)],

                DESC: [MessageHandler(Filters.text, desc), ],

                CMP: [MessageHandler(Filters.text, job_types)],
                JOBTYPES: [MessageHandler(Filters.regex('^(Remote|Permanent|Contractual|Hourly)$'), final)],
            },

            fallbacks=[CommandHandler('cancel', cancel)]
        )
        updater.dispatcher.add_handler(CommandHandler('cancel', cancel))
        updater.dispatcher.add_handler(conv_handler)
        updater.start_polling()
        updater.idle()
    else:
        messageSender()


if __name__ == "__main__":
    main()
