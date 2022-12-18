import sqlite3
from models import User


def get_user_by_id(id):
    conn = sqlite3.connect('db/users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM users WHERE id = ?'
    cursor.execute(sql, (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def get_user_by_email(email):
    conn = sqlite3.connect('db/users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM users WHERE email = ?'
    cursor.execute(sql, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def add_user(user):

    conn = sqlite3.connect('db/users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO users(nome,cognome,email,password) VALUES(?,?,?,?)'

    try:
        cursor.execute(
            sql, (user['name'], user['surname'], user['email'], user['password']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success
