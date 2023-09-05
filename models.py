from app import db
from flask_login import UserMixin


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
