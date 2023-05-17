from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
    InlineQueryHandler
)
from auth_data import token
import basic_handlers, additional_handlers


def run():
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", basic_handlers.start_message))

    dispatcher.add_handler(CallbackQueryHandler(additional_handlers.y_query, pattern="cb_yes"))
    dispatcher.add_handler(CallbackQueryHandler(additional_handlers.n_query, pattern="cb_no"))

    # dispatcher.add_handler(CallbackQueryHandler(handlers.main_dish_query, pattern="main_dish"))

    dispatcher.add_handler(CommandHandler("help", basic_handlers.help))
    dispatcher.add_handler(CommandHandler("end", basic_handlers.end))

    updater.start_polling()


run()


