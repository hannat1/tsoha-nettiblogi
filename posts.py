from db import db
from sqlalchemy.sql import text
import users

def get_list():
    #Feed view
    sql = text("SELECT P.id, P.title, P.content, U.username, P.sent_at FROM posts P, users U WHERE P.user_id=U.id AND P.visible=TRUE ORDER BY P.sent_at DESC")
    result = db.session.execute(sql)
    return result.fetchall()

def username(user_id):
    sql = text("SELECT U.username FROM users U WHERE U.id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()

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
    sql = text("SELECT P.id, P.title, P.content, P.sent_at FROM posts P WHERE P.user_id=:user_id AND P.visible=TRUE")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def followers(user_id):
    sql = text("SELECT U.username, U.id FROM users U, followings F WHERE F.follower_id=U.id AND F.followed_id=:user_id AND F.visible=TRUE")
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

def unfollow(user):
    #Unfollow a profile
    follower_id = users.user_id()
    followed_id = user
    sql = text("UPDATE followings SET visible=FALSE WHERE follower_id=:follower_id AND followed_id=:followed_id")
    db.session.execute(sql, {"follower_id":follower_id, "followed_id":followed_id})
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

def unlike(post_id):
    #Unlike a post
    print(post_id)
    user_id = users.user_id()
    sql = text("UPDATE likes SET visible=FALSE WHERE post_id=:post_id AND user_id=:user_id")
    db.session.execute(sql, {"post_id":post_id, "user_id":user_id})
    db.session.commit()
    return True

    
def likers_names(post):
    sql = text("SELECT U.username FROM users U, likes L WHERE L.user_id=U.id AND L.post_id=:post AND L.visible=TRUE")
    result = db.session.execute(sql, {"post":post})
    return result.fetchall()

def likers_ids(post):
    sql = text("SELECT U.id FROM users U, likes L WHERE L.user_id=U.id AND L.post_id=:post AND L.visible=TRUE")
    result = db.session.execute(sql, {"post":post})
    return result.fetchall()

def comment(comment, post_id):
    #Make comment on a post
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO comments (post_id, user_id, content, sent_at) VALUES (:post_id, :user_id, :content, NOW())")
    db.session.execute(sql, {"post_id":post_id, "user_id":user_id, "content":comment})
    db.session.commit()
    return True

def delete_comment(comment_id):
    #Delete a comment
    sql = text("UPDATE comments SET visible=FALSE WHERE id=:comment_id")
    db.session.execute(sql, {"comment_id":comment_id})
    db.session.commit()
    return True

def comments(post_id):
    # Get comments of a post
    sql = text("SELECT C.content, C.user_id, U.username, C.sent_at, C.id, P.id FROM comments C, posts P, users U WHERE C.post_id=P.id AND C.post_id=:post_id AND C.user_id=U.id AND C.visible=TRUE ORDER BY C.sent_at DESC")
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchall()

def delete_post(post_id):
    sql = text("UPDATE posts SET visible=FALSE WHERE id=:post_id")
    db.session.execute(sql, {"post_id":post_id})
    db.session.commit()
    return True

def filter_f():
    user_id = users.user_id()
    sql = text("SELECT DISTINCT P.id, P.title, P.content, U.username, P.sent_at FROM posts P, users U, followings F WHERE P.user_id IN (SELECT F.followed_id FROM followings F WHERE F.follower_id=:user_id AND F.visible=TRUE) AND P.user_id=U.id AND P.visible=TRUE ORDER BY P.sent_at DESC")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def filter_l():
    user_id = users.user_id()
    sql = text("SELECT DISTINCT P.id, P.title, P.content, U.username, P.sent_at  FROM posts P JOIN users U ON P.user_id = U.id JOIN likes L ON P.id = L.post_id WHERE L.user_id = :user_id AND L.visible = TRUE AND P.visible = TRUE ORDER BY P.sent_at DESC")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()
