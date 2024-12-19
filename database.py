import sqlite3

def add_user(id,username): #Добавление пользователя в таблицу
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id int, username VARCHAR(32))')

    # cur.execute("INSERT INTO users (user_id, username) VALUES ('%s', '%s')" % ('23242424', 'user1')) #тест 1
    # cur.execute(f"INSERT INTO users (user_id, username) VALUES ('\'111111\'', '%s')" % ('11111111', 'user2')) #тест 1

    conn.commit()
    cur.execute("INSERT INTO users (user_id, username) VALUES ('%s', '%s')" %(id,username))
    conn.commit()
    cur.close()
    conn.close()

    add_db_for_user(id)

def add_db_for_user(id): #Создание таблицы для определённого пользователя, с кем он встречался
    conn = sqlite3.connect(f'user{id}.sql')
    cur = conn.cursor()

    cur.execute(f'DROP TABLE IF EXISTS user{id}')  # Todo Удалить строчку перед выводом в продакшн

    cur.execute(f'CREATE TABLE IF NOT EXISTS user{id} (id INTEGER PRIMARY KEY, user_id int)')
    conn.commit()
    cur.close()
    conn.close()

def get_new_friend(id): #Получение линка напарника на эту неделю. Передаём id пользователя, для которого хотим получить напарника
    conn = sqlite3.connect(f'user{id}.sql')
    cur = conn.cursor()

    # cur.execute(f"INSERT INTO user{id} (user_id) VALUES ('%s')" %'23242424') #тест 1
    # cur.execute(f"INSERT INTO user{id} (user_id) VALUES ('%s')" % '11111111') #тест 1
    # conn.commit()

    cur.execute(f'SELECT COUNT(*) FROM user{id}')
    last = cur.fetchall()[0][0]
    cur.execute(f"SELECT user_id FROM user{id} WHERE id={last}")
    try:
        friend_id = cur.fetchall()[0][0]
        cur.close()
        conn.close()

        return get_username(friend_id)
    except IndexError:
        return 0

    return get_username(friend_id)

def get_username(id):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute(f'SELECT username FROM users where user_id = {id}')
    username = cur.fetchall()[0][0]

    cur.close()
    conn.close()

    return username