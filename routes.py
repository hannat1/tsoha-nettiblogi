from app import app
from flask import render_template, request, redirect, url_for
import posts, users, follows, likes, comments

@app.route("/")
def index():
    list = posts.get_list()
    user_id = users.user_id()
    username = users.username(user_id)
    return render_template("index.html", posts=list, user=(username, user_id))

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    title = request.form["title"]
    content = request.form["content"]
    if len(title) > 50:
        return render_template("error.html", message="Title is too long")
    if len(title) == 0:
        return render_template("error.html", message="Title is missing")
    if len(content) > 1000:
        return render_template("error.html", message="Message is too long")
    if len(content) == 0:
        return render_template("error.html", message="Content is missing")
    if posts.send(title, content):
        return redirect("/")
    else:
        return render_template("error.html", message="Post was not successful")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong password or username")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if 3>len(username):
            return render_template("error.html", message="Username is too short")
        if len(username)>13:
            return render_template("error.html", message="Username is too long")
        if 6>len(password1):
            return render_template("error.html", message="Password is too short")
        if len(password1)>20:
            return render_template("error.html", message="Password is too long")
        if password1 != password2:
            return render_template("error.html", message="Passwords differ")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Registering was not successful")
        
@app.route("/viewpost/<int:post_id>")
def view_post(post_id):
    list = posts.selectpost(post_id)
    list_comments = comments.comments(post_id)
    current_user = users.user_id()
    likers = likes.likers(post_id)
    like = False 
    for i in likers:
        if current_user == i[0]:
            like = True
    return render_template("/post.html", user=current_user, post=list, like = like, comments=list_comments, likes_amount= len(likers))

@app.route("/like/<int:post_id>")
def like(post_id):
    post = post_id
    if likes.like(post):
        return redirect(url_for("view_post", post_id=post_id))
    else:
        return render_template("error.html", message="Like was not successful")

@app.route("/unlike/<int:post_id>")
def unlike(post_id):
    if likes.unlike(post_id):
        return redirect(url_for("view_post", post_id=post_id))
    else:
        return render_template("error.html", message="Unlike was not successful")

@app.route("/viewprofile/<int:user_id>")
def view_profile(user_id):
    list = users.viewprofile(user_id)
    list_posts = posts.users_posts(user_id)
    list_followers = follows.followers(user_id)
    current_user = users.user_id()
    cannot_follow =False
    if current_user == user_id:
        cannot_follow = True
    follow = False
    for i in list_followers:
        if current_user == i[1]:
            follow = True
    return render_template("/profile.html", profile=list, posts=list_posts, followers_amount=len(list_followers), list_followers= list_followers, follow = follow, cannot_follow=cannot_follow)

@app.route("/follow/<int:user_id>")
def follow(user_id):
    user = user_id
    if follows.follow(user):
        return redirect(url_for("view_profile", user_id=user_id))
    else:
        return render_template("error.html", message="Following was not successful")

@app.route("/unfollow/<int:user_id>")
def unfollow(user_id):
    user = user_id
    if follows.unfollow(user):
        return redirect(url_for("view_profile", user_id=user_id))
    else:
        return render_template("error.html", message="Following was not successful")

@app.route("/comment/<int:post_id>", methods=["POST"])
def comment(post_id):
    comment = request.form["comment"]
    if len(comment) == 0:
        return render_template("error.html", message="Comment is missing")
    if comments.comment(comment, post_id):
        return redirect(url_for("view_post", post_id=post_id))
    else:
        return render_template("error.html", message="Comment was not successful")

@app.route("/del_comment/<int:post_id>/<int:comment_id>")
def delete_comment(post_id, comment_id):
    if comments.delete_comment(comment_id):
        return redirect(url_for("view_post", post_id=post_id))
    else:
        return render_template("error.html", message="Deleting comment was not successful")

@app.route("/del_post/<int:post_id>")
def delete_post(post_id):
    if posts.delete_post(post_id):
        return redirect("/")
    else:
        return render_template("error.html", message="Deleting post was not successful")

@app.route("/following")
def filter_following():
    followed_posts = follows.filter_f()
    return render_template("filtered.html", posts = followed_posts)

@app.route("/liked")
def filter_liked():
    liked_posts = likes.filter_l()
    return render_template("liked.html", liked_posts = liked_posts)

