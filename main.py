import os
import logging
from contextvars import ContextVar

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

import dialogflow_v2


logger = logging.getLogger('bot_logger')

TELEGRAM_TOKEN = os.environ['TELEGRAM_VERBS_TOKEN']
CHAT_ID = ContextVar('chat_id')

GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
DIALOGFLOW_PROJECT_ID = os.environ['DIALOGFLOW_PROJECT_ID']



class BotHandler(logging.Handler):
    def __init__(self, bot):
        logging.Handler.__init__(self)
        self._bot = bot

    def emit(self, record):
        msg = self.format(record)
        self._bot.send_message(chat_id=CHAT_ID.get(), text=msg)


class DialogflowHelper:
    def __init__(self, chat_id, msg):
        self._chat_id = chat_id
        self._msg = msg

        self._client = dialogflow_v2.SessionsClient()
        self._session = self._client.session_path(DIALOGFLOW_PROJECT_ID, self._chat_id)
        self._text_input = dialogflow_v2.types.TextInput(text=self._msg, language_code='ru')
        self._query_input = dialogflow_v2.types.QueryInput(text=self._text_input)

        self.response = self.detect_intent(self._client, self._session, self._query_input)

    def detect_intent(self, client=None, session=None, query_input=None):
        try:
            response = client.detect_intent(session=session, query_input=query_input)
        except:
            logger.debug(f'Something goes wrong:\n', exc_info=True)
            response = {}

        return response

    @property
    def query_text(self, response=None):
        if response is None:
            response = self.response

        try:
            result = response.query_result.query_text
        except:
            logger.debug('Cannot get the value of query_text:\n', exc_info=True)
            result = None

        return result

    @property
    def fulfillment_text(self, response=None):
        if response is None:
            response = self.response

        try:
            result = response.query_result.fulfillment_text
        except:
            logger.debug('Cannot get the value of fulfillment_text:\n', exc_info=True)
            result = None

        return result


def start(update, context):
    CHAT_ID.set(update.effective_chat.id)
    message = 'Здравствуйте!'
    return context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def greet(update, context):
    chat_id = update.effective_chat.id
    msg = update.message.text
    CHAT_ID.set(chat_id)

    df = DialogflowHelper(chat_id, msg)
    context.bot.send_message(chat_id=chat_id, text=df.fulfillment_text)


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

    message_handler = MessageHandler(Filters.text, greet)
    dispatcher.add_handler(message_handler)

    while True:
        try:
            updater.start_polling()
            updater.idle()
        except:
            pass
