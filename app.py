from flask import Flask, jsonify, redirect, render_template, request, session
from pymongo import MongoClient
import os
from passlib.hash import pbkdf2_sha512

from dotenv import load_dotenv


from course.route_course import add_course_routes
from professors.routes_professors import add_professor_routes
from students.routes_students import add_student_routes
from tutorial.routes_tutorial import add_tutorial_routes


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.permanent_session_lifetime = 60 * 60 * 24 * 7  # 1 week
app.debug = True
# MongoDB connection
client: MongoClient = MongoClient(
    os.getenv("MONGODB_URI", "").replace("'", "").replace('"', "")
)
db = client["mydatabase"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin", methods=["GET"])
def admin():
    """
    Route for admin login.
    """
    return render_template("admin.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Route for login.
    """
    session.pop("student", None)
    session.pop("professor", None)
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
        if data.get("isProf"):
            # Professor login
            prof = db.professors.find_one(
                {
                    "email": username,
                }
            )
            if not prof:
                return jsonify({"error": "Invalid username or password"}), 401
            if not pbkdf2_sha512.verify(password, prof["password"]):
                return jsonify({"error": "Invalid username or password"}), 401
            session["professor"] = prof["_id"]
            return jsonify({"message": "/professor/dashboard"}), 200
        else:
            # Student login
            student = db.students.find_one(
                {
                    "email": username,
                }
            )
            if not student:
                return jsonify({"error": "Invalid username or password"}), 401
            if not pbkdf2_sha512.verify(password, student["password"]):
                return jsonify({"error": "Invalid username or password"}), 401
            session["student"] = student["_id"]
            return jsonify({"message": "/student/dashboard"}), 200

    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    """
    Route for logout.
    """
    session.pop("student", None)
    session.pop("professor", None)
    return jsonify({"message": "Logout successful"}), 200


add_student_routes(app)
add_professor_routes(app)

# Add other routes
add_tutorial_routes(app)
add_course_routes(app)


@app.route("/home", methods=["GET"])
def home():
    """
    Route for home page.
    """
    if "student" in session:
        return redirect("/student/dashboard")
    if "professor" in session:
        return redirect("/professor/dashboard")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
