from sqlalchemy.sql import text
from db import db
import users

def followers(user_id):
    #Get followers of a user
    sql = text("""SELECT U.username, U.id FROM users U, followings F
               WHERE F.follower_id=U.id AND F.followed_id=:user_id AND F.visible=TRUE""")
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
    sql = text("""UPDATE followings SET visible=FALSE
               WHERE follower_id=:follower_id AND followed_id=:followed_id""")
    db.session.execute(sql, {"follower_id":follower_id, "followed_id":followed_id})
    db.session.commit()
    return True

def filter_f():
    #Filter posts by following
    user_id = users.user_id()
    sql = text("""SELECT DISTINCT P.id, P.title, P.content, U.username, P.sent_at
               FROM posts P, users U, followings F 
               WHERE P.user_id IN (SELECT F.followed_id FROM followings F WHERE F.follower_id=:user_id AND F.visible=TRUE) 
               AND P.user_id=U.id AND P.visible=TRUE ORDER BY P.sent_at DESC""")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()
