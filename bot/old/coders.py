#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This program is dedicated to handle coders neded new applications

import logging
import json
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ReplyKeyboardRemove,
                      KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler,
                          MessageHandler, Filters, ConversationHandler, CallbackContext)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# GENDER, PHOTO, LOCATION, BIO = range(4)
JNAME, JDESC, JCMP, JTYPE = range(4)

BOT_TOKEN = "1346826306:AAEBRd8TbKAl4t52gqZGginATw91dTWea38"
kb = [[
    KeyboardButton('📝 Add new job'),
    KeyboardButton('🧳 Your Job offers')],
    [KeyboardButton('⚙️ Settings')]]
kb_markup = ReplyKeyboardMarkup(kb, resize_keyboard=True)


def start(update, context):
    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n')

# handles job name


def entryTxt(update, context):
    command = update.message.text
    if command == "📝 Add new job":
        update.message.reply_text(
            "Enter /cancel to stop ")
        update.message.reply_text(
            "Enter the Name of the job: ", reply_markup=ReplyKeyboardRemove())
        return JNAME
    elif command == "🧳 Your Job offers":
        update.message.reply_text('Use /cancel to stop posting !')
        keyboard = [[KeyboardButton("Opened")],
                    [InlineKeyboardButton("Closed")],
                    [InlineKeyboardButton("Back To Menu")],
                    ]
        offer_markup = ReplyKeyboardMarkup(keyboard)

        update.message.reply_text(
            "select an option", reply_markup=offer_markup)
    elif command == "Back To Menu":
        update.message.reply_text(
            "select an option", reply_markup=kb_markup)
    elif command == "Opened":
        for data in searchJobs("opened"):
            message = """\nJob Title: {}\n\nCompany: {}\n\nJob Type: {}\n\nDescription: {}""".format(
                data['title'], data['company'], data['jobtype'], data['desc']
            )
            key = [[InlineKeyboardButton(
                "Close application", callback_data='close_application')]]
            update.message.reply_text(
                message, reply_markup=InlineKeyboardMarkup(key))

    elif command == "Closed":
        for data in searchJobs("closed"):
            message = """\nJob Title: {}\n\nCompany: {}\n\nJob Type: {}\n\nDescription: {}""".format(
                data['title'], data['company'], data['jobtype'], data['desc']
            )
            update.message.reply_text(message)


def postjob(update, context):
    # reply_keyboard = [['Boy', 'Girl', 'Other']]
    update.message.reply_text(
        "Enter /cancel to stop ")

    update.message.reply_text(
        "Enter the Name of the job: ", reply_markup=ReplyKeyboardRemove())

    return JNAME

# handles job description


def jname(update, context):
    # user = update.message.from_user
    context.user_data['job_name'] = update.message.text
    # logger.info("Job title is %s: %s", user.first_name, update.message.text)
    update.message.reply_text("Enter the job description here: ",
                              reply_markup=ReplyKeyboardRemove())

    return JDESC


# handles company name
def jdesc(update, context):
    user = update.message.from_user
    # logger.info("Photo of %s: %s", user.f)
    context.user_data['job_desc'] = update.message.text
    update.message.reply_text("Ennter the company name: ")

    return JCMP


# handles job type
def jcompany(update, context):
    user = update.message.from_user
    # logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
    #             user_location.longitude)
    context.user_data['company'] = update.message.text
    reply_keyboard = [['Contractual', 'Hourly', 'Remote', 'Premanent']]
    update.message.reply_text('What is the job type ?',
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard, one_time_keyboard=True))

    return JTYPE


def jtype(update, context):
    user = update.message.from_user
    context.user_data['job_type'] = update.message.text
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    query = update.callback_query
    data = context.user_data
    message = """\nJob Title: {}\n\nCompany: {}\n\nJob Type: {}\n\nDescription: {}""".format(
        data['job_name'], data['company'], data['job_type'], data['job_desc']
    )

    keyboard = [[InlineKeyboardButton("✅  Submit", callback_data='submit')],
                [InlineKeyboardButton("❌  Cancel", callback_data='cancel')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)
    update.message.reply_text(
        "check and submit your post", reply_markup=kb_markup)

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    # logger.info("Application progress cancelled use /postjob to try again",
    #             user.first_name)
    update.message.reply_text('Application progress cancelled use /postjob to try again',
                              reply_markup=kb_markup)

    return ConversationHandler.END


def callback_query_handler(update: Update, context: CallbackContext):
    call_message = update.callback_query.data
    if call_message == "submit":
        try:
            query = update.callback_query
            message = """!!!!!!!! SUBMITTED !!!!!!!!!!\n\n{}\n\n!!!!!!!! SUBMITTED !!!!!!!!!!""".format(
                update.callback_query.message.text
            )
            update.callback_query.edit_message_text(text=message)
            context.bot.answer_callback_query(
                callback_query_id=query.id, text="Your Job post is being verified by Admins Please wait ....",
                show_alert=True
            )
        except Exception as e:
            logger.warn(str(e))
    # close applicatoin on request
    elif call_message == "close_application":
        try:
            data = context.user_data
            message = """!!!!!!!! CLOSED !!!!!!!!!!\n\n{}\n\n!!!!!!!! CLOSED !!!!!!!!!!""".format(
                update.callback_query.message.text
            )
            update.callback_query.edit_message_text(
                text=message)
        except Exception as p:
            print(p)


def searchJobs(typ):
    jobs = []
    if typ == "opened":
        alljobs = json.load(
            open('/home/anonny/scrapers/coders_needed/data.json'))
        for data in alljobs:
            if data['opened'] == True:
                jobs.append(data)
    elif typ == "closed":
        alljobs = json.load(
            open('/home/anonny/scrapers/coders_needed/data.json'))
        for data in alljobs:
            if data['closed'] == True:
                jobs.append(data)

    return jobs


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    updater.dispatcher.add_handler(
        CallbackQueryHandler(callback_query_handler))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('postjob', postjob),
                      MessageHandler(Filters.text, entryTxt)],

        states={
            JNAME: [MessageHandler(Filters.text & ~Filters.command, jname)],

            JDESC: [MessageHandler(Filters.text & ~Filters.command, jdesc)],

            JCMP: [MessageHandler(Filters.text & ~Filters.command, jcompany)],

            JTYPE: [MessageHandler(Filters.regex(
                '^(Contractual|Hourly|Remote|Premanent)$'), jtype)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(callback_query_handler))
    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
