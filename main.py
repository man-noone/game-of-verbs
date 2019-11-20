import os
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


TELEGRAM_TOKEN = os.environ['TELEGRAM_VERBS_TOKEN']
logger = logging.getLogger('bot_logger')


def start(update, context):
    message = 'Здравствуйте!'
    return context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def main():
    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%d.%b.%Y %H:%M:%S')

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

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
