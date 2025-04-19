from functools import wraps
import uuid
from flask import Flask, jsonify, redirect, render_template, request, session
from pymongo import MongoClient
import os
from passlib.hash import pbkdf2_sha512

from dotenv import load_dotenv

from tutorial.tutorial import make_tutorial

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.permanent_session_lifetime = 60 * 60 * 24 * 7  # 1 week
app.debug = True
# MongoDB connection
client: MongoClient = MongoClient(os.getenv("MONGODB_URI"))
db = client["mydatabase"]

students_collection = db["students"]
professors_collection = db["professors"]


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


def student_login_required(f):
    """
    This decorator ensures that a user is logged in before accessing certain routes.
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        if "student" in session:
            return f(*args, **kwargs)
        else:
            return redirect("/")

    return wrap


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin", methods=["GET"])
def admin():
    """
    Route for admin login.
    """
    return render_template("admin.html")


@app.route("/create_tutorial", methods=["POST"])
def create_tutorial():
    """
    Route for creating a tutorial.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Call the make_tutorial function with the provided data
    tutorial_id = make_tutorial(data)

    return jsonify({"tutorial_id": tutorial_id}), 201

from students.routes_students import add_student_routes
from professors.routes_professors import add_professor_routes

add_student_routes(app)
add_professor_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
