from flask import jsonify, redirect, render_template, request, session

from course import course
import route_wrapper
from .models import Student


def add_student_routes(app):
    """Add student routes."""

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
        return Student().add_student(data)

    @app.route("/professor/update_student", methods=["POST"])
    def update_student():
        """
        Route for updating a student.
        """
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        email = data.get("email")
        courses = data.get("courses")

        if not email or not courses:
            return jsonify({"error": "Courses are required"}), 400

        return Student().update_student_course_info(data)

    @app.route("/student/dashboard", methods=["GET"])
    def student_dashboard():
        """
        Route for student dashboard.
        """
        if "student" not in session:
            return redirect("/student/login")

        return render_template("dash_stu.html")

    @app.route("/student/add_update_courses", methods=["GET", "POST"])
    @route_wrapper.student_login_required
    def student_add_update_courses():
        """
        Route for adding or updating courses.
        """
        if "student" not in session:
            return redirect("/student/login")

        if request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            courses = data.get("courses")

            if not courses:
                return jsonify({"error": "Courses are required"}), 400

            return Student().update_student_course_info(data)

        return render_template(
            "add_update_courses.html", courses=course.get_all_courses()
        )
