from app import app
from flask import render_template, request, redirect, url_for
import posts, users

@app.route("/")
def index():
    list = posts.get_list()
    return render_template("index.html", posts=list)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    title = request.form["title"]
    content = request.form["content"]
    if posts.send(title, content):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

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
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        
@app.route("/viewpost/<int:post_id>")
def view_post(post_id):
    list = posts.selectpost(post_id)
    current_user = users.user_id()
    list_likers_names = posts.likers_names(post_id)
    list_likers_ids = posts.likers_ids(post_id)
    print(list_likers_ids)
    like = False
    for i in list_likers_ids:
        if current_user == i[0]:
            like = True
    print(like)
    return render_template("/post.html", post=list, like = like)

@app.route("/like/<int:post_id>")
def like(post_id):
    post = post_id
    if posts.like(post):
        return redirect(url_for("view_post", post_id=post_id))
    else:
        return render_template("error.html", message="Like was not successful")


@app.route("/viewprofile/<int:user_id>")
def view_profile(user_id):
    list = posts.viewprofile(user_id)
    list_posts = posts.users_posts(user_id)
    list_followers_ids = posts.followers_ids(user_id)
    list_followers_names = posts.followers_names(user_id)
    current_user = users.user_id()
    cannot_follow =False
    if current_user == user_id:
        cannot_follow = True

    print(current_user, "current user")
    print(list_followers_ids, "ids")
    follow = False
    for i in list_followers_ids:
        if current_user == i[0]:
            follow = True
            
    return render_template("/profile.html", profile=list, posts=list_posts, followers_amount=len(list_followers_ids), list_followers_names = list_followers_names, list_followers_ids= list_followers_ids, follow = follow, cannot_follow=cannot_follow)

@app.route("/follow/<int:user_id>")
def follow(user_id):
    user = user_id
    if posts.follow(user):
        return redirect(url_for("view_profile", user_id=user_id))
    else:
        return render_template("error.html", message="Following was not successful")

