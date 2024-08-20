from db import db
from sqlalchemy.sql import text
import users

def like(post):
    #Like a post
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO likes (post_id, user_id) VALUES (:post, :user)")
    db.session.execute(sql, {"post":post, "user":user_id})
    db.session.commit()
    return True

def unlike(post_id):
    #Unlike a post
    print(post_id)
    user_id = users.user_id()
    sql = text("UPDATE likes SET visible=FALSE WHERE post_id=:post_id AND user_id=:user_id")
    db.session.execute(sql, {"post_id":post_id, "user_id":user_id})
    db.session.commit()
    return True

def likers(post):
    sql = text("SELECT U.id FROM users U, likes L WHERE L.user_id=U.id AND L.post_id=:post AND L.visible=TRUE")
    result = db.session.execute(sql, {"post":post})
    return result.fetchall()

def filter_l():
    user_id = users.user_id()
    sql = text("SELECT DISTINCT P.id, P.title, P.content, U.username, P.sent_at  FROM posts P JOIN users U ON P.user_id=U.id JOIN likes L ON P.id=L.post_id WHERE L.user_id=:user_id AND L.visible=TRUE AND P.visible=TRUE ORDER BY P.sent_at DESC")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()
