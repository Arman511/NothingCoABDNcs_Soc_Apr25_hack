from functools import wraps
from flask import Flask, jsonify, redirect, render_template, request, session
from pymongo import MongoClient
import os
from passlib.hash import pbkdf2_sha512

from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.permanent_session_lifetime = 60 * 60 * 24 * 7  # 1 week
# MongoDB connection
client: MongoClient = MongoClient(os.getenv("MONGODB_URI"))
db = client["mydatabase"]


def prof_login_required(f):
    """
    This decorator ensures that a user is logged in before accessing certain routes.
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        if "professor" in session:
            return f(*args, **kwargs)
        else:
            return redirect("/")

    return wrap


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/professor/login", methods=["GET", "POST"])
def professor_login():
    """
    Route for professor login.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        prof = db.proffessor.find_one(
            {
                "username": username,
            }
        )

        if prof is None:
            return jsonify({"error": "Invalid username or password"}), 401
        if pbkdf2_sha512.verify(password, prof["password"]):
            session["professor"] = username

            return redirect("/professor/dashboard")

    return render_template("professor_login.html")
