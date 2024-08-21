from db import db
from sqlalchemy.sql import text
import users

def feed():
    #Feed view
    sql = text("SELECT P.id, P.title, P.content, U.username, P.sent_at FROM posts P, users U WHERE P.user_id=U.id AND P.visible=TRUE ORDER BY P.sent_at DESC")
    result = db.session.execute(sql)
    return result.fetchall()

def send(title, content):
    #Make new post
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO posts (title, content, user_id, sent_at) VALUES (:title, :content, :user_id, NOW())")
    db.session.execute(sql, {"title":title, "content":content, "user_id":user_id})
    db.session.commit()
    return True

def selectpost(post_id):
    #Select post for viewing
    sql = text("SELECT P.id, P.title, P.content, U.username, U.id, P.sent_at FROM posts P, users U WHERE P.id =:post_id AND P.user_id=U.id")
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchone()

def users_posts(user_id):
    #Select all posts of a user
    sql = text("SELECT P.id, P.title, P.content, P.sent_at FROM posts P WHERE P.user_id=:user_id AND P.visible=TRUE")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def delete_post(post_id):
    sql = text("UPDATE posts SET visible=FALSE WHERE id=:post_id")
    db.session.execute(sql, {"post_id":post_id})
    db.session.commit()
    return True

def search(search):
    sql = text("SELECT P.id, P.title, P.user_id FROM posts P WHERE P.title LIKE (:search) AND P.visible=TRUE")
    result = db.session.execute(sql, {"search": "%"+search+"%"})
    return result.fetchall()