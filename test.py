from main import db_facade

for i in range(1,100):
        db_facade.add_user(i,i)
