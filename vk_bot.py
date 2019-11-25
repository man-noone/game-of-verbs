import os
import logging
from time import time_ns

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from main import DialogflowHelper


vk_logger = logging.getLogger('vk_logger')

VK_TOKEN = os.environ['VK_VERBS_TOKEN']

vk_session = vk_api.VkApi(token=VK_TOKEN)
vk_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def df_answer(event):
    df = DialogflowHelper(event.user_id, event.text)
    if df.fulfillment_text == 'Даже не знаю, что на это сказать':
        pass
    else:
        vk_api.messages.send(user_id=event.user_id,
                             message=df.fulfillment_text,
                             random_id=time_ns())



if __name__ == '__main__':
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    df_answer(event)
        except Exception as e:
            vk_logger.debug('Exception:\n', exc_info=True)
