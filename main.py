import os
import logging
from contextvars import ContextVar

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


TELEGRAM_TOKEN = os.environ['TELEGRAM_VERBS_TOKEN']
CHAT_ID = ContextVar('chat_id')
logger = logging.getLogger('bot_logger')


class BotHandler(logging.Handler):
    def __init__(self, bot):
        logging.Handler.__init__(self)
        self._bot = bot

    def emit(self, record):
        msg = self.format(record)
        self._bot.send_message(chat_id=CHAT_ID.get(), text=msg)


def start(update, context):
    CHAT_ID.set(update.effective_chat.id)
    message = 'Здравствуйте!'
    return context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def echo(update, context):
    CHAT_ID.set(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%d.%b.%Y %H:%M:%S')

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    bot = updater.bot

    bot_handler = BotHandler(bot)
    bot_handler.setLevel(logging.DEBUG)
    logger.addHandler(bot_handler)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    message_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(message_handler)

    while True:
        try:
            updater.start_polling()
            updater.idle()
        except:
            pass
