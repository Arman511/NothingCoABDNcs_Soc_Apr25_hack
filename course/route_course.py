from flask import jsonify, render_template, request

from course import course
import route_wrapper


def add_course_routes(app):
    """
    Add routes to the app.
    """

    @app.route("/add_course", methods=["GET", "POST"])
    @route_wrapper.prof_login_required
    def add_course():
        """
        Route for adding a course.
        """

        if request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            # Call the add_course function with the provided data
            result = course.add_course(data)

            return jsonify(result), 201

        return render_template("add_course.html")
