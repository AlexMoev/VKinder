from vk_api.utils import get_random_id

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from bd import create_db , add_user, add_view
from utils import check_info, search_people, get_photos

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
    info = ''
    res = []

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
                elif request == 'поиск':
                    if info:
                        message_send(event.user_id, "Начинаем поиск людей...")
                        res = search_people(info)
                        message_send(event.user_id, "Поиск закончен, напишите 'след' для показа")
                    else:
                        message_send(event.user_id, "Для начала проверьте информацию, для этого напишите 'начать'")
                elif request == 'след':
                    if res:
                        message_send(event.user_id, "Начинаем показ")
                        profile = res[0]
                        res = res[1:]
                        photos = get_photos(profile['id'])
                        add_view(event.user_id, profile['id'])
                        message_send(event.user_id, profile['name'])
                        message_send(event.user_id, profile['url'])
                        
                        for j in photos:
                            message_send(event.user_id, j['url'])


                    else:
                        message_send(event.user_id, "Еще/уже нет подходящих людей, осуществите поиск, для этого напишите 'поиск")
                else:
                    message_send(event.user_id, "Не понял вашего ответа...")


if __name__ == '__main__':
    main()

