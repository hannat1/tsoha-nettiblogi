import secrets
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql = text("SELECT id, password, visible FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    print(user)
    if user[2] == False:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["csrf_token"] = secrets.token_hex(16)
        return True
    return False

def logout():
    del session["user_id"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username,password) VALUES (:username,:password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def user_name(user):
    sql = text("SELECT U.username FROM users U WHERE U.id=:user_id")
    result = db.session.execute(sql, {"user_id":user})
    return result.fetchone()

def viewprofile(user):
    sql = text("SELECT U.id, U.username FROM users U WHERE U.id=:id AND U.visible=TRUE")
    result = db.session.execute(sql, {"id":user})
    return result.fetchone()

def search_user(search):
    sql = text("""SELECT U.id, U.username, COUNT(P.id)
                FROM posts P, users U
                WHERE U.visible = TRUE 
                AND P.visible = TRUE 
                AND U.id=P.user_id
                AND (lower(username) LIKE lower(:search))
                GROUP BY U.id
                """)
    result = db.session.execute(sql, {"search": "%"+search+"%"})
    return result.fetchall()

def del_user(user):
    sql = text("UPDATE users SET visible=FALSE WHERE id=:user_id")
    db.session.execute(sql, {"user_id":user})
    db.session.commit()
    return True