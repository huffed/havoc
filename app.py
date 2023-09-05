from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from config import mysql
from sqlalchemy import text
from flask_login import login_user, LoginManager, login_required, logout_user
from flask_argon2 import Argon2
from models import *
from forms import *

app = Flask(__name__)
argon2 = Argon2(app)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{mysql['username']}:{mysql['password']}@{mysql['host']}:{mysql['port']}/{mysql['schema']}"
app.config["SECRET_KEY"] = "havoc3141"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and argon2.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = argon2.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html", form=form)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
