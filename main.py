from vk_api.longpoll import VkEventType

from bd import add_offset, add_user, add_view, check_profile, create_db
from utils import check_info, get_photos, longpoll, message_send, search_people


def main():

    create_db()
    info = ''
    res = []

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text.lower()

                if request in ['привет', 'хай', 'добрый день', 'дарова']:
                    message_send(
                        event.user_id,
                        'Привет, для поиска людей напиши "начать"'
                    )

                elif request == "начать":
                    message_send(event.user_id, "Проверяем информацию...")
                    info = check_info(event.user_id)
                    add_user(info)
                    city = info['city']
                    age = info['age']
                    gender = info['gender']
                    relation = info['relation']
                    message_send(
                        event.user_id,
                        f"Ищем {city}, {age}, {gender}, {relation}"
                    )
                    message_send(
                        event.user_id,
                        "Готово! Напишите 'поиск' для старта"
                    )
                elif request == 'поиск':
                    if info:
                        message_send(event.user_id, "Начинаем поиск людей...")
                        res = search_people(info)
                        message_send(
                            event.user_id,
                            "Поиск закончен, напишите 'след' для показа"
                        )
                    else:
                        message_send(
                            event.user_id,
                            "Проверьте данные, для этого напишите 'начать'"
                        )
                elif request == 'след':
                    if res:
                        profile = res[0]
                        res = res[1:]
                        not_shown = check_profile(event.user_id, profile['id'])
                        if not_shown:
                            photos = get_photos(profile['id'])
                            add_view(event.user_id, profile['id'])
                            message_send(event.user_id, "Начинаем показ")
                            message_send(event.user_id, profile['name'])
                            message_send(event.user_id, profile['url'])

                            for j in photos:
                                message_send(event.user_id, j['url'])
                        else:
                            add_offset(event.user_id)

                    else:
                        message_send(
                            event.user_id,
                            "Еще/уже нет подходящих людей, напишите 'поиск"
                        )
                else:
                    message_send(event.user_id, "Не понял вашего ответа...")


if __name__ == '__main__':
    main()
