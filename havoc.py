from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_limiter import Limiter
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from utils.sql_connect import mysql_uri
from argon2 import PasswordHasher, Type

app = Flask(__name__)
app.config["SECRET_KEY"] = "havoc"

"""
MySQL DB
"""
app.config["SQLALCHEMY_DATABASE_URI"] = mysql_uri
mysql_db = SQLAlchemy(app)

limiter = Limiter(
    lambda: str(request.remote_addr),
    app=app,
    storage_uri="memory://",
)

cache = Cache(app, config={
    "CACHE_TYPE": "simple"
})

hasher = PasswordHasher(
    hash_len=30,
    salt_len=10,
    type=Type.ID
)


@app.route('/')
@cache.cached(timeout=120)
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        # add encryption to password form and integrate with a database
        select_query = text("""
                            select username, password from users where username = :username
                            """)
        valid_check = mysql_db.session.execute(
            select_query, {"username": request.form.get("username")}).fetchone()
        try:
            hasher.verify(valid_check[1], request.form.get("password"))
            return redirect(url_for("dashboard"))
        except:
            error = "Username or password not found."
            return render_template("login.html", error=error)
    else:
        return render_template("login.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        # add checks for if all fields are filled, then check if username is available, then check if password is good
        # goodnight xoxo

        username = request.form.get('username')
        if len(username) <= 2:
            return render_template('register.html', error_message="Username must be at least 3 characters long.")

        invite_key = request.form.get('invite key')
        select_query = text("""
                            """)

        insert_statement = text("""
                                INSERT INTO users (username, password, invite) VALUES (:username, :password, :invite)
                                """)
        data = {
            "username": request.form.get("username"),
            "password": hasher.hash(request.form.get("password")),
            "invite": request.form.get("invite key")
        }
        # connection.execute(insert_statement, parameters=data)
        # connection.commit()
        return redirect('/dashboard')
    else:
        return render_template('register.html')


@app.route('/check_availability', methods=['GET'])
@limiter.limit(limit_value="500 per hour")
def check_availability():
    select_query = text("""
                        select username from users where username = :username
                        """)

    # add different process for when its coming from register or login
    # check = connection.execute(select_query, parameters={username: request.form.get('username')}

    # add check for if result returns anything, if it does, return taken, otherwise say remove the error message

    response = {
        "availability": True,
        "origin": "register"
    }
    return jsonify(response)


def show_input(value):
    print(value)
    return value


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
