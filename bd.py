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
            Sp VARCHAR(40) NOT NULL,
            Offset INTEGER
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
    sql = '''
        DELETE FROM Users
        WHERE ID_User = (?)
    '''
    cursor.execute(sql, (user_id,))
    data = cursor.fetchall()
    if not data:
        sql = '''
            INSERT INTO Users(ID_User, Age, Gender, City, Sp, Offset)
            VALUES (?,?,?,?,?,?)
        '''
        cursor.execute(sql, (user_id, info['age'], info['gender'],
                             info['city'], info['relation'], 0))
        conn.commit()


def get_offset(user_id):
    sql = '''
        SELECT Offset FROM Users
        WHERE ID_User = (?)
    '''
    cursor.execute(sql, (user_id,))
    offset = cursor.fetchall()[0][0]
    return offset


def add_offset(user_id):
    offset = get_offset(user_id)

    sql = '''
        UPDATE Users
        SET Offset = (?)
        WHERE ID_User = (?)
    '''
    cursor.execute(sql, (offset + 1, user_id,))
    conn.commit()


def add_view(user_id, profile_id):
    sql = '''
        INSERT INTO Views(ID_User,ID_Profile)
        VALUES (?,?)
    '''
    cursor.execute(sql, (user_id, profile_id))
    conn.commit()
    add_offset(user_id)


def get_user(user_id):
    sql = '''
        SELECT * FROM Users
        WHERE ID_User = (?)
    '''
    cursor.execute(sql, (user_id,))
    data = cursor.fetchall()
    return data[0]


def check_profile(user_id, profile_id):
    sql = '''
        SELECT * FROM Views
        WHERE ID_User = (?) AND ID_Profile = (?)
    '''
    cursor.execute(sql, (user_id, profile_id))
    data = cursor.fetchall()
    if data:
        return False
    return True


if __name__ == '__main__':
    create_db()
