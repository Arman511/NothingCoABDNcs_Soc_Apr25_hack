from flask import jsonify, render_template, request, session

from course import course
import route_wrapper
from students.models import Student
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

            return jsonify({"tutorial_id": tutorial_id}), 200

        return render_template(
            "add_tutorial.html", courses=course.get_all_courses_ids()
        )

    @app.route("/tutorials/search", methods=["GET"])
    @route_wrapper.prof_login_required
    def get_tutorials():
        """
        Route for getting all tutorials.
        """
        tutorials = tutorial.get_all_tutorials()
        if not tutorials:
            return jsonify({"error": "No tutorials found"}), 404
        return render_template(
            "tutorials.html",
            tutorials=tutorials,
        )

    @app.route("/tutorials/my_tutorials", methods=["GET"])
    @route_wrapper.student_login_required
    def get_my_tutorials():
        """
        Route for getting all tutorials.
        """
        tutorials = tutorial.get_all_tutorials()
        if not tutorials:
            return jsonify({"error": "No tutorials found"}), 404

        student_uuid = session.get("student")
        student = tutorial.get_student_by_uuid(student_uuid)
        my_tut = []

        for tut in tutorials:
            if tut["course"] in student["courses"]:
                my_tut.append(tut)

        return render_template(
            "my_tutorials.html",
            tutorials=my_tut,
        )

    @app.route("/tutorials/update_record", methods=["GET", "POST"])
    @route_wrapper.student_login_required
    def update_tutorial_record():
        """
        Route for updating a tutorial record.
        """
        from app import db

        uuid = request.args.get("uuid")
        if not uuid:
            return jsonify({"error": "No UUID provided"}), 400

        if request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            # Call the update_tutorial function with the provided data
            return tutorial.update_student_tutorial(data, uuid)

        student_uuid = session.get("student")
        student_rec = Student().get_student_by_uuid(student_uuid)
        if not student_rec:
            return jsonify({"error": "No student found"}), 404
        tutorial_rec = db.tutorial_student.find_one(
            {"tutorial_id": uuid, "student_id": student_uuid}
        )

        if not tutorial_rec:
            new_tut = tutorial.get_tutorial_by_uuid(uuid)

            if not new_tut:
                return jsonify({"error": "No tutorial found"}), 404

            course_rec = db.courses.find_one({"course_id": new_tut["course"]})

            if course_rec["_id"] not in student_rec["courses"]:
                return jsonify({"error": "You are not enrolled in this course"}), 403

            tutorial_rec = {
                "tutorial_id": new_tut["_id"],
                "student_id": student_uuid,
                "tutorial_name": new_tut["tutorial_name"],
                "tutorial_due_date": new_tut["tutorial_due_date"],
                "tutorial_release_date": new_tut["tutorial_release_date"],
                "tutorial_answer_release_date": new_tut["tutorial_answer_release_date"],
                "course": new_tut["course"],
            }
            return render_template(
                "update_record_tutorial.html",
                tutorial=tutorial_rec,
            )

        return render_template(
            "update_record_tutorial.html",
            tutorial=tutorial_rec,
        )
