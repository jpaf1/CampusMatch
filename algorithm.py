import database
import pandas as pd

#df_set - множество всех пользоватей
#S - множество уже обработанных пользователей
#user_set - множество людей, с кем встречался этот пользователь

def alg():
    conn = database.sqlite3.connect('database.sql')
    table = pd.read_sql("SELECT * FROM users",con=conn)
    conn.close()

    df = table['user_id']
    df_set = set(df)
    #print(len(df_set))
    S = set()

    twice_user = -1
    #обработка случая, когда количество пользователей нечётно
    if len(df_set)%2==1:
        print("Кто пойдёт на две встречи? (укажите user_id)")
        twice_user = int(input())

    for user in df:
        if user not in S:
            S.add(user)
            conn = database.sqlite3.connect(f'user{user}.sql')
            user_df = pd.read_sql(f"SELECT * FROM user{user}",con=conn)['user_id']
            conn.close()
            user_set = set(user_df)
            strangers = (df_set - S) - user_set
            if len(strangers) > 0:
                new_friend = strangers.pop()
                S.add(new_friend)
            else:
                new_friend = twice_user
            #Добавление друг друга в таблицы
            #внизу обработка для текущего пользователя
            conn = database.sqlite3.connect(f'user{user}.sql')
            cur = conn.cursor()
            cur.execute(f"INSERT INTO user{user} (user_id) VALUES ('%s')" % (new_friend))
            conn.commit()
            cur.close()
            conn.close()
            #внизу обработка для другого пользователя
            conn = database.sqlite3.connect(f'user{new_friend}.sql')
            cur = conn.cursor()
            cur.execute(f"INSERT INTO user{new_friend} (user_id) VALUES ('%s')" % (user))
            conn.commit()
            cur.close()
            conn.close()