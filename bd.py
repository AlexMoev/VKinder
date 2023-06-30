import sqlite3


conn = sqlite3.connect('vkinder.db')
cursor = conn.cursor()

def create_db():
    # Создание таблицы пользователей
    sql = '''
        CREATE TABLE IF NOT EXISTS Users(
            ID_User PRIMARY KEY,
            Age INTEGER NOT NULL,
            Gender VARCHAR(40) NOT NULL,
            City VARCHAR(40) NOT NULL,
            Sp VARCHAR(40) NOT NULL
        );
    '''
    cursor.execute(sql)

    # Создание таблицы просмотров профилей
    sql = '''
        CREATE TABLE IF NOT EXISTS Views(
            ID_View SERIAL PRIMARY KEY,
            ID_User integer references Users(ID_User),
            ID_Profile INTEGER NOT NULL
        );
    '''
    cursor.execute(sql)


def add_user(info):
    user_id = info['user_id']
    sql = f'''
        SELECT * FROM Users
        WHERE ID_User = (?)
    '''
    cursor.execute(sql, (user_id,))
    data = cursor.fetchall()
    print(data)
    if not data:
        sql = '''
            INSERT INTO Users(ID_User, Age, Gender, City, Sp)
            VALUES (?,?,?,?,?)
        '''
        cursor.execute(sql, (user_id, info['age'], info['gender'], info['city'], info['relation']))
        conn.commit()










if __name__ == '__main__':
    create_db()
