import vk_api


vk = vk_api.VkApi(token = 'vk1.a.qeg0kp7u7ImOpcqlLBwcY-x9uESnX7ELM8sr0rkz4V1XPaI8DWztpC-1eUTZLpTWY3XK-pwPvqygiDPbvBStVy42B7bcCSqKhi1CqyPYrM2FbIkoYHrwo8CJ9Q2EPEdZiYvgtl7kiSq8aGR6ryWiMiy97OTOvAVMGJk4TYA06uyxVp2J0urdSFLZ3bbOM8mlpI6kKOwsRO0-IpGTLRDl9A')
    


from datetime import date

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
    city = user_get[0]['city']['title']
    gender = user_get[0]['sex']
    relation = user_get[0]['relation']
    if gender == 2:
        find_gender = 1
    else:
        find_gender = 2
    return {
        'age': age,
        'city': city,
        'gender': find_gender,
        'relation': relation,
        'user_id': user_id
    }

