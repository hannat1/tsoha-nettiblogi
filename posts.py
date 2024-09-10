from sqlalchemy.sql import text
from db import db
import users

def feed():
    sql = text("""SELECT P.id, P.title, P.content, U.username, P.sent_at
               FROM posts P
               JOIN users U ON P.user_id=U.id
               WHERE U.visible=TRUE AND P.visible=TRUE 
               ORDER BY P.sent_at DESC""")
    result = db.session.execute(sql)
    return result.fetchall()

def send(title, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("""INSERT INTO posts (title, content, user_id, sent_at)
               VALUES (:title, :content, :user_id, NOW())""")
    db.session.execute(sql, {"title":title, "content":content, "user_id":user_id})
    db.session.commit()
    return True

def selectpost(post_id):
    sql = text("""SELECT P.id, P.title, P.content, U.username, U.id, P.sent_at
               FROM posts P, users U WHERE P.id =:post_id AND P.user_id=U.id""")
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchone()

def users_posts(user_id):
    sql = text("""SELECT P.id, P.title, P.content, P.sent_at
               FROM posts P WHERE P.user_id=:user_id AND P.visible=TRUE
               ORDER BY P.sent_at DESC""")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def delete_post(post_id):
    sql = text("UPDATE posts SET visible=FALSE WHERE id=:post_id")
    db.session.execute(sql, {"post_id":post_id})
    db.session.commit()
    return True

def search_post(search):
    sql = text("""SELECT P.id, P.title, P.content, P.user_id, U.username
                FROM posts P, users U
                WHERE P.visible=TRUE AND U.visible=TRUE
                AND U.id=P.user_id
                AND
                (lower(title) LIKE lower(:search)
                OR
                lower(content) LIKE lower(:search))
                """)
    result = db.session.execute(sql, {"search": "%"+search+"%"})
    return result.fetchall()
