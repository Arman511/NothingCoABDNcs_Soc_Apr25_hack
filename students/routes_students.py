import uuid
from dotenv import load_dotenv
from flask import jsonify, redirect, render_template, request, session
from itsdangerous import URLSafeSerializer
from passlib.hash import pbkdf2_sha512
from .models import Student


def add_student_routes(app):
    """Add student routes."""

    @app.route("/add_student", methods=["POST"])
    def add_student():
        """
        Route for adding a student.
        """
        from app import db

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

            student = db.students_collection.find_one(
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
        


