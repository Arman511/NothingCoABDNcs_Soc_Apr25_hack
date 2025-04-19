from flask import jsonify, redirect, render_template, request, session
from passlib.hash import pbkdf2_sha512
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

    @app.route("/student/login", methods=["GET", "POST"])
    def student_login():
        """
        Route for student login.
        """
        from app import db

        if request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            username = data.get("username")
            password = data.get("password")
            if not username or not password:
                return jsonify({"error": "Username and password are required"}), 400

            student = db.students.find_one(
                {
                    "email": username,
                }
            )

            if student is None:
                return jsonify({"error": "Invalid username or password"}), 401
            if pbkdf2_sha512.verify(password, student["password"]):
                session["student"] = username

                return redirect("/student/dashboard")

        return render_template("login_stu.html")

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
    
    @app.route("/student/mycourses", methods=["GET"]) 
    def student_mycourses():
        """
        Route for student courses.
        """
        if "student" not in session:
            return redirect("/student/login")
        
        student_courses = Student().get_student_courses(session["student"])
        if not student_courses:
            return jsonify({"error": "No courses found"}), 404
        
        return render_template("mycourses_stu.html", courses=student_courses)
        
        
        

