from flask import jsonify, render_template, request

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

    @app.route("/professor/dashboard", methods=["GET"])
    @route_wrapper.prof_login_required
    def professor_dashboard():
        """
        Route for professor dashboard.
        """
        return render_template("dash_prof.html")
