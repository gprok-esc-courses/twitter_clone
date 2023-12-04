from flask import Flask, render_template, request, redirect, session, g
from database import *
import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "kdjfdlkjhfsdkjhfdskj56kjsdhdskjhfkjs"
app.config['SESSION_TYPE'] = 'filesystem'
bcrypt = Bcrypt(app) 

create_db()
create_tables()

def check_loggedin_user():
    username = session.get("username")
    if username is None:
        g.user = None
    else:
        g.user = get_user(username)

@app.route("/feed")
def feed():
    check_loggedin_user()
    tweets = get_all_tweets()
    return render_template('feed.html', tweets=tweets)

@app.route("/register", methods=['GET', 'POST'])
def register():
    check_loggedin_user()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        birthdate = request.form.get('birthdate')
        try:
            datetime.date.fromisoformat(birthdate)
        except ValueError:
            return render_template("register.html", message="Incorrect data format, should be YYYY-MM-DD")
        if password != password2:
            return render_template("register.html", message="Passwords do not match.")
        else:
            user = get_user(username)
            if user is not None:
                return render_template("register.html", message="Username already taken.")
            else:
                add_user(username, bcrypt.generate_password_hash(password).decode('utf-8'), birthdate)
                return redirect("/login")
    else:
        return render_template("register.html")
    

@app.route("/login", methods=['GET', 'POST'])
def login():
    check_loggedin_user()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)
        if user is None:
            return render_template("login.html", message="User not found")
        else:
            if bcrypt.check_password_hash(user[2], password):
                session["username"] = username
                return redirect("/feed")
            else:
                return render_template("login.html", message="Wrong password")      
    else:
        return render_template("login.html")
    
@app.route("/tweet", methods=['POST'])
def tweet():
    check_loggedin_user()
    # check if there is a user
    text = request.form.get('tweet')
    add_tweet(text, g.user[0])
    return redirect("/feed")

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/feed")
