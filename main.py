from vk_api.utils import get_random_id

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = input('Token: ')

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


# def write_msg(user_id, message):
#     vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

def message_send(user_id, message, attachment=None):
    vk.method('messages.send',
        {
            'user_id': user_id,
            'message': message,
            'attachment': attachment,
            'random_id': get_random_id()
        }
    )


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                message_send(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                message_send(event.user_id, "Пока((")
            else:
                message_send(event.user_id, "Не поняла вашего ответа...")