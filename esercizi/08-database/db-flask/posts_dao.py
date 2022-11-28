import sqlite3

def get_posts():
  conn = sqlite3.connect('db/blog.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  sql = 'SELECT * FROM posts ORDER BY date DESC'
  cursor.execute(sql)
  posts = cursor.fetchall()
  #print(posts)

  cursor.close()
  conn.close()

  return posts

def get_post(id):
  conn = sqlite3.connect('db/blog.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  sql = 'SELECT * FROM posts WHERE id = ?'
  cursor.execute(sql, (id,))
  post = cursor.fetchone()

  cursor.close()
  conn.close()

  return post

def add_post(post):
  conn = sqlite3.connect('db/blog.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  success = False
  sql = 'INSERT INTO posts(title,date,tag,content,user_id) VALUES(?,?,?,?,?)'

  try:
    cursor.execute(sql, (post['title'], post['date'], post['tag'], post['content'],1))
    conn.commit()
    success = True
  except Exception as e:
    print('ERROR', str(e))
    # if something goes wrong: rollback
    conn.rollback()

  cursor.close()
  conn.close()

  return success

def get_comments(id):
  conn = sqlite3.connect('db/blog.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  sql = 'SELECT content FROM comments WHERE post_id = ?'
  cursor.execute(sql, (id,))
  comments = cursor.fetchall()

  cursor.close()
  conn.close()

  return comments