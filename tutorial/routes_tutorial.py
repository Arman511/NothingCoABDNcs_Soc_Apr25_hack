from flask import jsonify, render_template, request

from course import course
import route_wrapper
from tutorial import tutorial


def add_tutorial_routes(app):
    """
    Add routes to the app.
    """

    @app.route("/tutorials/add_tutorial", methods=["GET", "POST"])
    @route_wrapper.prof_login_required
    def add_tutorial():
        """
        Route for adding a tutorial.
        """
        if request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            # Call the make_tutorial function with the provided data
            tutorial_id = tutorial.make_tutorial(data)

            return jsonify({"tutorial_id": tutorial_id}), 201

        return render_template(
            "add_tutorial.html", courses=course.get_all_courses_ids()
        )
