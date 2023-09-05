from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from models.user import User
from extensions import argon2


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
    username = StringField(validators=[InputRequired()], render_kw={
                           "placeholder": "username"})

    password = PasswordField(validators=[InputRequired()], render_kw={
                             "placeholder": "password"})

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if existing_user_username is None or not argon2.check_password_hash(existing_user_username.password, str(self.password.data)):
            raise ValidationError("Username or password incorrect.")

    submit = SubmitField("submit")
