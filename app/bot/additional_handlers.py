from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext


def y_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    update.callback_query.message.reply_text('👍 Приступимо')
    return_my_songs(update, context)



def n_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    update.callback_query.message.reply_text('👋 Не цього разу')


def return_my_songs(update: Update, context: CallbackContext):
    pass



def main(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()


