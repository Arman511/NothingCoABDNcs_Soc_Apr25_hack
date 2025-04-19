from flask import jsonify, redirect, render_template, request, session
from passlib.hash import pbkdf2_sha512

import route_wrapper
from .models import Professor


def add_professor_routes(app):
    """Add professor routes."""

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

        return Professor().register_professor(data)

    @app.route("/professor/logout", methods=["GET"])
    def logout():
        """
        Route for logging out.
        """
        session.pop("professor", None)
        return redirect("/")

    @app.route("/professor/dashboard", methods=["GET"])
    @route_wrapper.prof_login_required
    def professor_dashboard():
        """
        Route for professor dashboard.
        """
        return render_template("professor_dashboard.html")

    @app.route("/professor/login", methods=["GET", "POST"])
    def professor_login():
        """
        Route for professor login.
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

            prof = db.professors_collection.find_one(
                {
                    "email": username,
                }
            )

            if prof is None:
                return jsonify({"error": "Invalid username or password"}), 401
            if pbkdf2_sha512.verify(password, prof["password"]):
                session["professor"] = username

                return redirect("/professor/dashboard")

        return render_template("login_prof.html")
