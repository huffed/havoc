from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from config import mysql
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from sqlalchemy import text
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_argon2 import Argon2

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


class User(db.Model, UserMixin):
    __tablename__ = "users"
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    avatar = db.Column(db.String(200), nullable=False, default="")
    usergroup = db.Column(db.SmallInteger, nullable=False, default=0)

    def get_id(self):
        return self.uid

    def __repr__(self):
        return f"<User {self.username}>"


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=3, max=20, message=None)], render_kw={"placeholder": "username"})

    password = PasswordField(validators=[InputRequired(), EqualTo("confirm", message="Passwords don't match"), Length(
        min=4)], render_kw={"placeholder": "password"})

    confirm = PasswordField(render_kw={"placeholder": "confirm password"})

    submit = SubmitField("submit")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if existing_user_username:
            raise ValidationError("Username already exists.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=3, max=20)], render_kw={"placeholder": "username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4)], render_kw={"placeholder": "password"})

    submit = SubmitField("submit")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if argon2.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("dashboard"))

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
