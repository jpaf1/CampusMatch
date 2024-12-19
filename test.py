import algorithm
import database

for i in range(100):
        database.add_user(i, i)

algorithm.alg()

pairs = set()

for id in range(100):
    new_friend = database.get_new_friend(id)
    if (f'{id}', new_friend) not in pairs and (new_friend, f'{id}') not in pairs:
        pairs.add((f'{id}', new_friend))

print(pairs)

algorithm.alg()

pairs1 = set()

for id in range(100):
    new_friend = database.get_new_friend(id)
    if (f'{id}', new_friend) not in pairs1 and (new_friend, f'{id}') not in pairs1:
        pairs1.add((f'{id}', new_friend))

print(pairs1)

print(len(pairs), len(pairs1))