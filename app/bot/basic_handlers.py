from telegram import Update, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext


def start_message(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Так", callback_data="cb_yes"),
         InlineKeyboardButton('Ні', callback_data='cb_no')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Привіт! 🎵🐈 Хотіли б почати роботу?", reply_markup=reply_markup)


HELP_MESSAGE = """
<b>Вітаємо в MusicLibrary!🎵🐈</b>
Для навігації ботом можете використовувати наступні команди:

/start - почати
/help - допомога
/end - закінчити
""".format()


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        HELP_MESSAGE,
        parse_mode=ParseMode.HTML
    )


BYE_MESSAGE = """
Дякуємо за ваш час! До нових зустрічей 😻
"""


def end(update: Update, context: CallbackContext):
    update.message.reply_text(
        BYE_MESSAGE,
        parse_mode=ParseMode.HTML
    )









