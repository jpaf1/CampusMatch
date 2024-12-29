import sqlite3
import pandas as pd

class PairingAlgorithm:
    @staticmethod
    def match_users(twice_user):

        # df_set - множество всех пользоватей
        # S - множество уже обработанных пользователей
        # user_set - множество людей, с кем встречался этот пользователь

        conn = sqlite3.connect('database.sql')
        df = pd.read_sql('SELECT user_id FROM users', conn)
        conn.close()

        df_set = set(df['user_id'])
        S = set()
        pairs = []

        for user in df_set:
            if user not in S:
                S.add(user)
                user_conn = sqlite3.connect(f'user{user}.sql')
                user_data = pd.read_sql('SELECT user_id FROM user_links', user_conn)
                user_conn.close()
                user_set = set(user_data['user_id'])
                available = (df_set - S) - user_set

                if available:
                    friend = available.pop()
                else:
                    friend = twice_user

                pairs.append((user, friend))

                #Добавляем обоих в БД каждого пользователя
                PairingAlgorithm._add_link(user, friend)
                PairingAlgorithm._add_link(friend, user)

        print(pairs)

    @staticmethod
    def _add_link(user, friend): #добавление нового друга в БД пользователя
        with sqlite3.connect(f'user{user}.sql') as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO user_links (user_id) VALUES (?)', (friend,))