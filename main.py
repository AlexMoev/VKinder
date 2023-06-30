from vk_api.utils import get_random_id

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from bd import create_db , add_user
from utils import check_info

# token = input('Token: ')
token = 'vk1.a.ReYtNDXCf2maJG1nSzhPYZWtABVbvyN562voJRhO8j2ahBDQaj7XS1Y4dt077_mh0umLzACWzjR0ckH0SIDOSGyLodJKukkISvtKycNSpvnCOaCclVQxndp0IAZqSAGegwrx156vl21y0CgzFLPcV35I9WoQbjzK1JybxKgxWXjHLava5AwaoJTCAoYxpfNAlvEHjcWArANDyRJld4Ji8w'

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


def main():

    create_db()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text.lower()

                if request in ['привет', 'хай', 'добрый день', 'дарова']:
                    message_send(event.user_id, f'Привет, для поиска людей напиши "начать"')

                elif request == "начать":
                    message_send(event.user_id, "Проверяем информацию...")
                    info = check_info(event.user_id)
                    add_user(info)
                    message_send(event.user_id, f"Ищем {info['city']}, {info['age']}, {info['gender']}, {info['relation']}")
                    message_send(event.user_id, "Готово! Напишите 'поиск' для старта")
                else:
                    message_send(event.user_id, "Не понял вашего ответа...")


if __name__ == '__main__':
    main()