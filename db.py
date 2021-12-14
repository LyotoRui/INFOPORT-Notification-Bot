import sqlite3

users = sqlite3.connect('users.db')
curs = users.cursor()

def init_db():
    curs.execute('''CREATE TABLE IF NOT EXISTS users(
        users TEXT 
    )''')
    users.commit()

def insert_user(id):
    curs.execute('''INSERT INTO users(users) VALUES(?)''', (id))
    users.commit()
