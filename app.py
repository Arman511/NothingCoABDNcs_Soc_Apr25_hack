from functools import wraps
from flask import Flask, jsonify, redirect, render_template, request, session
from pymongo import MongoClient
import os
from passlib.hash import pbkdf2_sha512

from dotenv import load_dotenv

from tutorial import make_tutorial

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


@app.route("/student/login", methods=["GET", "POST"])
def student_login():
    """
    Route for student login.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        student = db.students.find_one(
            {
                "username": username,
            }
        )

        if student is None:
            return jsonify({"error": "Invalid username or password"}), 401
        if pbkdf2_sha512.verify(password, student["password"]):
            session["student"] = username

            return redirect("/student/dashboard")

    return render_template("student_login.html")


@app.route("/admin", methods=["GET"])
def admin():
    """
    Route for admin login.
    """
    return render_template("admin.html")


@app.route("/professor/dashboard", methods=["GET"])
@prof_login_required
def professor_dashboard():
    """
    Route for professor dashboard.
    """
    return render_template("professor_dashboard.html")


@app.route("/logout", methods=["GET"])
def logout():
    """
    Route for logging out.
    """
    session.pop("professor", None)
    return redirect("/")


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


@app.route("/add_student", methods=["POST"])
def add_student():
    """
    Route for adding a student.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check if the student already exists
    if db.students.find_one({"email": email}):
        return jsonify({"error": "Student already exists"}), 400

    # Hash the password and save the student
    hashed_password = pbkdf2_sha512.hash(password)
    db.students.insert_one({"email": email, "password": hashed_password})

    return jsonify({"message": "Student added successfully"}), 201


@app.route("/add_professor", methods=["POST"])
def add_professor():
    """
    Route for adding a professor.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check if the professor already exists
    if db.proffessor.find_one({"email": email}):
        return jsonify({"error": "Professor already exists"}), 400

    # Hash the password and save the professor
    hashed_password = pbkdf2_sha512.hash(password)
    db.proffessor.insert_one({"email": email, "password": hashed_password})

    return jsonify({"message": "Professor added successfully"}), 201
