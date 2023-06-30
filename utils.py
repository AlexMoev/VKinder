import vk_api

from datetime import date
from bd import get_user, get_offset

vk = vk_api.VkApi(token = 'vk1.a.qeg0kp7u7ImOpcqlLBwcY-x9uESnX7ELM8sr0rkz4V1XPaI8DWztpC-1eUTZLpTWY3XK-pwPvqygiDPbvBStVy42B7bcCSqKhi1CqyPYrM2FbIkoYHrwo8CJ9Q2EPEdZiYvgtl7kiSq8aGR6ryWiMiy97OTOvAVMGJk4TYA06uyxVp2J0urdSFLZ3bbOM8mlpI6kKOwsRO0-IpGTLRDl9A')
    


def calculate_age(born):
    today = date.today()
    born = born.split('.')
    born = date(int(born[2]), int(born[1]), int(born[0]))
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def check_info(user_id):
    user_get = vk.method('users.get',
                            {'user_id': user_id,
                            'fields': 'city,bdate,sex,relation' 
                            }
                            )

    age = user_get[0]['bdate']
    age = calculate_age(age)
    city = user_get[0]['city']['id']
    gender = user_get[0]['sex']
    relation = user_get[0]['relation']
    return {
        'age': age,
        'city': city,
        'gender': gender,
        'relation': relation,
        'user_id': user_id
    }

def search_people(user_info):
    user_info['gender'] = 1 if user_info['gender'] == 2 else 2
    offset = get_offset(user_info['user_id'])
    users = vk.method('users.search',
                                {'count': 10,
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
        if user['is_closed'] == False:
            res.append(
                {
                    'id' : user['id'],
                    'name': user['first_name'] + ' ' + user['last_name'],
                    'url': f'https://vk.com/id{user["id"]}'
                }
            )
    
    return res


def get_photos(user_id):
    photos = vk.method('photos.get',
                                {'user_id': user_id,
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
