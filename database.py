import sqlite3

class Database: #работа с базой данных
    def __init__(self):
        self.user_db = 'database.sql'

    def add_user(self, user_id, username): #добавление пользователя в общую базу
        with sqlite3.connect(self.user_db) as conn:
            cur = conn.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id INTEGER, username TEXT)')
            cur.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', (user_id, username))

        self._create_user_table(user_id)

    def _create_user_table(self, user_id): #создание БД для конкретного пользователя
        with sqlite3.connect(f'user{user_id}.sql') as conn:
            cur = conn.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS user_links (id INTEGER PRIMARY KEY, user_id INTEGER)')

    def get_new_friend(self, user_id):
        try:
            with sqlite3.connect(f'user{user_id}.sql') as conn:
                cur = conn.cursor()

                # Получение последнего id записи
                cur.execute('SELECT MAX(id) FROM user_links')
                last_id = cur.fetchone()[0]

                if last_id is None:
                    return None  # Если таблица пуста, возвращаем None

                # Получение id друга по последней записи
                cur.execute('SELECT user_id FROM user_links WHERE id = ?', (last_id,))
                friend_id = cur.fetchone()

                if friend_id and friend_id[0]:
                    return self.get_username(friend_id[0])
                else:
                    return None
        except sqlite3.Error as e:
            print(f"Error fetching new friend for user_id {user_id}: {e}")
            return None

    def get_username(self, user_id):
        try:
            with sqlite3.connect('database.sql') as conn:
                cur = conn.cursor()

                # Получение имени пользователя
                cur.execute('SELECT username FROM users WHERE user_id = ?', (user_id,))
                result = cur.fetchone()

                return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error fetching username for user_id {user_id}: {e}")
            return None

