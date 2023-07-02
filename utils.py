from datetime import date

import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

from bd import get_offset
from config import group_token, user_token

vk = vk_api.VkApi(token=user_token)
vk_group = vk_api.VkApi(token=group_token)
longpoll = VkLongPoll(vk_group)


def message_send(user_id, message, attachment=None):
    vk_group.method(
        'messages.send',
        {
            'user_id': user_id,
            'message': message,
            'attachment': attachment,
            'random_id': get_random_id()
        }
    )


def calculate_age(born):
    today = date.today()
    born = born.split('.')
    born = date(int(born[2]), int(born[1]), int(born[0]))
    add_one = (today.month, today.day) < (born.month, born.day)
    return today.year - born.year - add_one


def check_info(user_id):
    user_get = vk.method(
        'users.get',
        {
            'user_id': user_id,
            'fields': 'city,bdate,sex,relation'
        }
    )

    age = user_get[0]['bdate']
    if not age:
        age = get_user_age(user_id)
    age = calculate_age(age)
    city = user_get[0]['city']
    if not city:
        city = get_user_city(user_id)
    city = city['id']
    gender = user_get[0]['sex']
    if not gender:
        gender = get_user_gender(user_id)
    relation = user_get[0]['relation']
    return {
        'age': age,
        'city': city,
        'gender': gender,
        'relation': relation,
        'user_id': user_id
    }


def search_people(user_info):
    if user_info['gender'] == 1:
        user_info['gender'] = 2
    elif user_info['gender'] == 2:
        user_info['gender'] = 1
    offset = get_offset(user_info['user_id'])
    users = vk.method(
        'users.search',
        {
            'count': 10,
            'offset': offset,
            'age_from': user_info['age'],
            'age_to': user_info['age'],
            'sex': user_info['gender'],
            'city': user_info['city'],
            'status': 6,
            'is_closed': False
        }
    )
    try:
        users = users['items']
    except KeyError:
        return []

    res = []

    for user in users:
        if not user['is_closed']:
            res.append(
                {
                    'id': user['id'],
                    'name': user['first_name'] + ' ' + user['last_name'],
                    'url': f'https://vk.com/id{user["id"]}'
                }
            )

    return res


def get_photos(user_id):
    photos = vk.method(
        'photos.get',
        {
            'user_id': user_id,
            'album_id': 'profile',
            'extended': 1
        }
    )
    try:
        photos = photos['items']
    except KeyError:
        return []

    res = []

    for photo in photos:
        res.append(
            {
                'owner_id': photo['owner_id'],
                'id': photo['id'],
                'likes': photo['likes']['count'],
                'comments': photo['comments']['count'],
                'url': photo['sizes'][-1]['url']
            }
        )

    res.sort(key=lambda x: x['likes']+x['comments']*10, reverse=True)
    return res[:3]


def get_user_age(user_id):
    message_send(
        user_id,
        'Мы не знаем ваш возраст, введите свой возраст в формате дд.мм.гггг:'
    )
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text.lower()
                if request[2] == request[5] == '.':
                    if request.replace('.', '').isdigit():
                        return request
                else:
                    message_send(
                        user_id,
                        'Введите возраст в формате дд.мм.гггг'
                    )


def get_user_city(user_id):
    message_send(user_id, 'Мы не знаем ваш город, введите свой город:')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text.lower()
                cities = vk.method(
                    'database.getCities',
                    {
                        'country_id': 1,
                        'q': request,
                        'need_all': 1,
                        'count': 5000
                    }
                )['items']
                for city in cities:
                    if city['title'].lower() == request:
                        return city

                message_send(user_id, 'Мы не знаем этот город, введите другой')


def get_user_gender(user_id):
    message_send(
        user_id,
        'Введите 0 для любого пола, 1 для женского и 2 для мужского:'
    )
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text.lower()
                if request == '1' or request == '2':
                    return request
                message_send(user_id, 'Введите цифру 0, 1 или 2')
