from flask import Flask, render_template
from pymongo import MongoClient
import os

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
client: MongoClient = MongoClient(os.getenv("MONGODB_URI"))
db = client["mydatabase"]

students_collection = db["students"]
professors_collection = db["professors"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin", methods=["GET"])
def admin():
    """
    Route for admin login.
    """
    return render_template("admin.html")


add_student_routes(app)
add_professor_routes(app)

# Add other routes
add_tutorial_routes(app)
add_course_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
