from flask import render_template, request, redirect, url_for, session, abort
from app import app
import posts
import users
import follows
import likes
import comments

@app.route("/")
def index():
    feed_filter = False
    feed_list = posts.feed()
    user_id = users.user_id()
    username = users.user_name(user_id)
    return render_template("index.html", posts=feed_list,
                           user=(username, user_id), filter=feed_filter)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
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
        if len(username) < 3 or len(username) > 16:
            return render_template("error.html", message="Username is not of valid length")
        if len(password1) < 4 or len(password1) > 20:
            return render_template("error.html", message="Password is not of valid length")
        if password1 != password2:
            return render_template("error.html", message="Passwords differ")
        if users.register(username, password1):
            return redirect("/")
    return render_template("error.html", message="Registering was not successful")

@app.route("/viewpost/<int:post_id>")
def view_post(post_id):
    post = posts.selectpost(post_id)
    list_comments = comments.comments(post_id)
    current_user = users.user_id()
    likers = likes.likers(post_id)
    liked = False
    for i in likers:
        if current_user == i[0]:
            liked = True
    return render_template("/post.html", user=current_user, post=post,
                           liked=liked, comments=list_comments, likes_amount= len(likers))

@app.route("/like/<int:post_id>")
def like(post_id):
    if likes.like(post_id):
        return redirect(url_for("view_post", post_id=post_id))
    return render_template("error.html", message="Like was not successful")

@app.route("/unlike/<int:post_id>")
def unlike(post_id):
    if likes.unlike(post_id):
        return redirect(url_for("view_post", post_id=post_id))
    return render_template("error.html", message="Removing like was not successful")

@app.route("/viewprofile/<int:user_id>")
def view_profile(user_id):
    profile = users.viewprofile(user_id)
    list_posts = posts.users_posts(user_id)
    list_followers = follows.followers(user_id)
    total_likes = likes.total_likes(user_id)
    current_user = users.user_id()
    cannot_follow =False
    if current_user == user_id:
        cannot_follow = True
    followed = False
    for i in list_followers:
        if current_user == i[1]:
            followed = True
    return render_template("/profile.html", profile=profile, posts=list_posts,
                           followers_amount=len(list_followers), list_followers=list_followers,
                           follow=followed, cannot_follow=cannot_follow, total_likes=total_likes)

@app.route("/follow/<int:user_id>")
def follow(user_id):
    if follows.follow(user_id):
        return redirect(url_for("view_profile", user_id=user_id))
    return render_template("error.html", message="Following was not successful")

@app.route("/unfollow/<int:user_id>")
def unfollow(user_id):
    if follows.unfollow(user_id):
        return redirect(url_for("view_profile", user_id=user_id))
    return render_template("error.html", message="Following was not successful")

@app.route("/comment/<int:post_id>", methods=["POST"])
def comment(post_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    content = request.form["comment"]
    if len(content) == 0:
        return render_template("error.html", message="Comment is missing")
    if comments.comment(content, post_id):
        return redirect(url_for("view_post", post_id=post_id))
    return render_template("error.html", message="Comment was not successful")

@app.route("/del_comment/<int:post_id>/<int:comment_id>")
def delete_comment(post_id, comment_id):
    if comments.delete_comment(comment_id):
        return redirect(url_for("view_post", post_id=post_id))
    return render_template("error.html", message="Deleting comment was not successful")

@app.route("/del_post/<int:post_id>")
def delete_post(post_id):
    if posts.delete_post(post_id):
        return redirect("/")
    return render_template("error.html", message="Deleting post was not successful")

@app.route("/filter")
def filter_following():
    feed_filter = True
    user_id = users.user_id()
    username = users.user_name(user_id)
    followed_posts = follows.filter_f()
    return render_template("index.html", posts=followed_posts,
                           user=(username, user_id), filter=feed_filter)

@app.route("/liked")
def filter_liked():
    user_id = users.user_id()
    liked_posts = likes.filter_l()
    return render_template("liked.html", liked_posts=liked_posts, user=user_id)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        content = request.args["search"]
        result_posts = posts.search_post(content)
        result_users = users.search_user(content)
        return render_template("result.html", search=content, posts=result_posts, users=result_users)
    return render_template("search.html")

@app.route("/del_account", methods=["GET", "POST"])
def delete_account():
    if request.method == "POST":
        confirmation = request.form["confirmation"]
        user_id = users.user_id()
        if confirmation == "yes":
            if users.del_user(user_id):
                users.logout()
                return redirect("/")
        return redirect(url_for("view_profile", user_id=user_id))
    return render_template("delete_account.html")
