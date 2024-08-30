from sqlalchemy.sql import text
from db import db
import users

def comment(content, post_id):
    #Make comment on a post
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("""INSERT INTO comments (post_id, user_id, content, sent_at)
               VALUES (:post_id, :user_id, :content, NOW())""")
    db.session.execute(sql, {"post_id":post_id, "user_id":user_id, "content":content})
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
    sql = text("""SELECT C.content, C.user_id, U.username, C.sent_at, C.id, P.id
               FROM comments C, posts P, users U 
               WHERE C.post_id=P.id AND C.post_id=:post_id 
               AND C.user_id=U.id AND C.visible=TRUE 
               ORDER BY C.sent_at""")
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchall()
