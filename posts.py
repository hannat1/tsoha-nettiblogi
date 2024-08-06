from db import db
from sqlalchemy.sql import text
import users

def get_list():
    sql = text("SELECT P.id, P.title, P.content, U.username, P.sent_at FROM posts P, users U WHERE P.user_id=U.id ORDER BY P.sent_at DESC")
    result = db.session.execute(sql)
    return result.fetchall()

def send(title, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO posts (title, content, user_id, sent_at) VALUES (:title, :content, :user_id, NOW())")
    db.session.execute(sql, {"title":title, "content":content, "user_id":user_id})
    db.session.commit()
    return True

def selectpost(post_id):
    sql = text("SELECT P.id, P.title, P.content, P.user_id, P.sent_at FROM posts P WHERE P.id =:post_id")
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchone()