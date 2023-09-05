from flask_sqlalchemy import SQLAlchemy

mysql = {
    "username": "jack",
    "password": "Cr1m1n4ls",
    "host": "192.168.1.208",
    "port": "3306",
    "schema": "admin"
}


db = SQLAlchemy()
