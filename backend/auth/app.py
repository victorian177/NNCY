from flask import Flask, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

PSTGRS_USERNAME = os.getenv("POSTGRES_USERNAME")
PSTGRS_DATABASE = os.getenv("POSTGRES_DATABASE")
PSTGRS_PASSWORD = os.getenv("POSTGRES_PASSWORD")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{PSTGRS_USERNAME}:{PSTGRS_PASSWORD}@localhost:5432/{PSTGRS_DATABASE}"


db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user_data'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)

    def __init__(self, first_name, last_name, email, password_hash):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return f"{self.first_name} {self.last_name}: {self.email}"
        

@app.route("/signup", methods=["GET", "POST"])
def signup():
    message = {}
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password_hash = generate_password_hash(request.form.get("password"))

    email_query = User.query.filter_by(email=email).first()


    if email_query is not None:
        message = {"Error": "Email already exists in database! Please login."}
    else:
        user_data = User(first_name=first_name, last_name=last_name, email=email, password_hash=password_hash)

        db.session.add(user_data)
        db.session.commit()

        usr_data = str(user_data).split(': ')
        message[usr_data[0]] = usr_data[1]

    return message

@app.route("/login", methods=["GET", "POST"])
def login():
    message = {}
    email = request.form.get("email")

    email_query = User.query.filter_by(email=email).first()

    if not email_query or check_password_hash(email_query.password_hash, request.form.get("password")):
        message["Error"] = "Please check your login details and try again."
    else:
        message[email] = "Logged in"

    return message

if __name__ == "__main__":
    app.run(debug=True, port=5000)
