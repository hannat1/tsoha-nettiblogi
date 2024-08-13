from db import db
from sqlalchemy.sql import text
import users

def get_list():
    #Feed view
    sql = text("SELECT P.id, P.title, P.content, U.username, P.sent_at FROM posts P, users U WHERE P.user_id=U.id ORDER BY P.sent_at DESC")
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

def viewprofile(user_id):
    #Select profile for viewing
    sql = text("SELECT U.id, U.username FROM users U WHERE U.id=:id")
    result = db.session.execute(sql, {"id":user_id})
    return result.fetchone()

def users_posts(user_id):
    #Select all posts of a user
    sql = text("SELECT P.id, P.title, P.content, P.sent_at FROM posts P WHERE P.user_id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def followers_names(user_id):
    sql = text("SELECT U.username FROM users U, followings F WHERE F.follower_id=U.id AND F.followed_id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def followers_ids(user_id):
    sql = text("SELECT F.follower_id FROM followings F WHERE F.followed_id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def follow(user):
    #Follow a profile
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO followings (follower_id, followed_id) VALUES (:user_id, :user)")
    db.session.execute(sql, {"user_id":user_id, "user":user})
    db.session.commit()
    return True

def like(post):
    #Like a post
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO likes (post_id, user_id) VALUES (:post, :user)")
    db.session.execute(sql, {"post":post, "user":user_id})
    db.session.commit()
    return True
    
def likers_names(post):
    sql = text("SELECT U.username FROM users U, likes L WHERE L.user_id=U.id AND L.post_id=:post")
    result = db.session.execute(sql, {"post":post})
    return result.fetchall()

def likers_ids(post):
    sql = text("SELECT U.id FROM users U, likes L WHERE L.user_id=U.id AND L.post_id=:post")
    result = db.session.execute(sql, {"post":post})
    return result.fetchall()