import sqlite3
import datetime

# Operazioni sui Post


def get_posts():
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT posts.id, posts.data_pubblicazione, posts.testo, posts.immagine_post, utenti.nickname, utenti.immagine_profilo FROM posts LEFT JOIN utenti ON posts.id_utente = utenti.id ORDER BY data_pubblicazione DESC'
    cursor.execute(sql)
    posts = cursor.fetchall()

    cursor.close()
    conn.close()

    return posts


def get_post(id):
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT posts.id, posts.data_pubblicazione, posts.testo, posts.immagine_post, posts.id_utente, utenti.nickname, utenti.immagine_profilo FROM posts LEFT JOIN utenti ON posts.id_utente = utenti.id WHERE posts.id = ?'
    cursor.execute(sql, (id,))
    post = cursor.fetchone()

    cursor.close()
    conn.close()

    return post


def add_post(post):
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    if 'immagine_post' in post:
        sql = 'INSERT INTO posts(data_pubblicazione,testo,immagine_post,id_utente) VALUES(?,?,?,?)'
        cursor.execute(sql, (post['data_pubblicazione'],
                             post['testo'], post['immagine_post'], post['id_utente']))
    else:
        sql = 'INSERT INTO posts(data_pubblicazione,testo,id_utente) VALUES(?,?,?)'
        cursor.execute(sql, (post['data_pubblicazione'],
                             post['testo'], post['id_utente']))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

# Operazioni sui Commenti


def get_comments(id):
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT commenti.id, commenti.data_pubblicazione, commenti.testo, utenti.nickname, utenti.immagine_profilo  FROM commenti LEFT JOIN utenti ON commenti.id_utente = utenti.id WHERE commenti.id_post = ?'
    cursor.execute(sql, (id,))
    comments = cursor.fetchall()

    cursor.close()
    conn.close()

    return comments


def add_comment(comment, id_utente):
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False

    x = datetime.datetime.now()

    sql = 'INSERT INTO commenti(data_pubblicazione,testo,id_post,id_utente) VALUES(?,?,?,?)'
    cursor.execute(sql, (x.strftime("%Y-%m-%d"),
                         comment['testo'], comment['id_post'], id_utente))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

# Funzione ausiliare per cercare l'id di un utente dato il suo nickname


def get_user_by_nickname(nickname):
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM utenti WHERE nickname = ?'
    cursor.execute(sql, (nickname,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def get_user_by_id(id):
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM utenti WHERE id = ?'
    cursor.execute(sql, (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def add_user(user):

    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO utenti(nickname,password,immagine_profilo) VALUES(?,?,?)'

    try:
        cursor.execute(
            sql, (user['nickname'], user['password'], user['immagine_profilo']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success
