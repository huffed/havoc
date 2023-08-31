from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, text
from utils.sql_connect import mysql
from argon2 import PasswordHasher, Type
import secrets
import string

app = Flask(__name__)

db_url = f"mysql+mysqlconnector://{mysql['username']}:{mysql['password']}@{mysql['hostname']}:{mysql['port']}/{mysql['schema']}"
engine = create_engine(db_url)

# connection = engine.connect()

hasher = PasswordHasher(
    hash_len=30,
    salt_len=10,
    type=Type.ID
)


def check_availability(username):
    select_query = text("select * from users where username = :username")
    # result = connection.execute(select_query, {"username": username}).fetchone()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = request.form.get("u")
        password = request.form.get("p")
        # add encryption to password form and integrate with a database
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        # add checks for if all fields are filled, then check if username is available, then check if password is good
        # goodnight xoxo

        username = request.form.get('u')
        if len(username) <= 2:
            return render_template('register.html', error_message="Username must be at least 3 characters long.")

        insert_statement = text(
            "INSERT INTO admin.users (username, password, invite) VALUES (:username, :password, :invite)")
        data = {
            "username": request.form.get("u"),
            "password": hasher.hash(request.form.get("p")),
            "invite": request.form.get("k")
        }
        # connection.execute(insert_statement, parameters=data)
        # connection.commit()
        return redirect('/dashboard')
    else:
        return render_template('register.html', error_message=None)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
