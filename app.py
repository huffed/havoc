from forms.user_forms import RegisterForm, LoginForm
from forms.edit_profile_forms import UploadForm
from models.user import User
from flask import Flask, render_template, url_for, redirect, request
from config import mysql
from sqlalchemy import text
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from database import db
from extensions import argon2
from flask_s3 import FlaskS3
import boto3
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO

app = Flask(__name__)
argon2.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{mysql['username']}:{mysql['password']}@{mysql['host']}:{mysql['port']}/{mysql['schema']}"
app.config["SECRET_KEY"] = "havoc3141"

db.init_app(app)

app.config["AWS_ACCESS_KEY_ID"] = "AKIA5NW22PD7HVMVIEF2"
app.config["AWS_SECRET_ACCESS_KEY"] = "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"
app.config["FLASKS3_BUCKET_NAME"] = "havoc-1"
s3 = FlaskS3(app)

s3_client = boto3.client(
    's3',
    aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"]
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


def get_s3_image(bucket_name, file_name):
    obj = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    return obj["Body"].read()


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
    return redirect("/")


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


@app.route("/@<username>")
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first()

    if user:
        return render_template("user-profile.html", user=user, username=user.username, uid=user.uid, avatar=s3_client.generate_presigned_url('get_object', Params={'Bucket': app.config["FLASKS3_BUCKET_NAME"], 'Key': user.avatar}, ExpiresIn=100))


@app.route("/@<username>/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile(username):
    """
    CROPPING IS FUCKED
    reference: http://127.0.0.1:5000/@evo
    """

    form = UploadForm()

    if form.validate_on_submit():
        image = form.image.data

        if image:
            cropped_image = Image.open(image)

            width, height = cropped_image.size
            crop_width, crop_height = 184, 184

            size = min(width, height)
            left = (width - size) / 2
            upper = (width - size) / 2
            right = (width + size) / 2
            lower = (width + size) / 2

            cropped_image = cropped_image.crop(
                (left, upper, right, lower))

            cropped_image = cropped_image.resize((crop_width, crop_height))

            filename = secure_filename(image.filename)

            image_data = BytesIO()

            cropped_image.save(image_data, format="PNG")

            image_data.seek(0)

            if current_user.avatar != 'default.png':
                s3_client.delete_object(
                    Bucket=app.config["FLASKS3_BUCKET_NAME"],
                    Key=current_user.avatar
                )

            s3_client.upload_fileobj(
                image_data,
                app.config["FLASKS3_BUCKET_NAME"],
                filename
            )

            current_user.avatar = filename
            db.session.commit()

            cropped_image.close()
            image_data.close()

    return render_template("edit-profile.html", form=form)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user, username=current_user.username, uid=current_user.uid, avatar=s3_client.generate_presigned_url('get_object', Params={'Bucket': app.config["FLASKS3_BUCKET_NAME"], 'Key': current_user.avatar}, ExpiresIn=100))


if __name__ == "__main__":
    app.run(debug=True)
