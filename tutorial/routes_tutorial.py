from datetime import datetime
import uuid
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
            return tutorial.make_tutorial(data)

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

        target_uuid = request.args.get("uuid")
        if not target_uuid:
            return jsonify({"error": "No UUID provided"}), 400

        if request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400

            # Call the update_tutorial function with the provided data
            return tutorial.update_student_tutorial(data, target_uuid)

        student_uuid = session.get("student")
        student_rec = Student().get_student_by_uuid(student_uuid)
        if not student_rec:
            return jsonify({"error": "No student found"}), 404

        tut = tutorial.get_tutorial_by_uuid(target_uuid)
        tutorial_student_rec = db.tutorial_student.find_one(
            {"tutorial_id": target_uuid, "student_id": student_uuid}
        )

        if not tutorial_student_rec:

            if not tut:
                return jsonify({"error": "No tutorial found"}), 404

            course_rec = db.courses.find_one({"course_id": tut["course"]})

            if course_rec["_id"] not in student_rec["courses"]:
                return jsonify({"error": "You are not enrolled in this course"}), 403

            tutorial_student_rec = {
                "_id": uuid.uuid4().hex,
                "tutorial_id": tut["_id"],
                "student_id": student_uuid,
                "tutorial_name": tut["tutorial_name"],
                "tutorial_due_date": tut["tutorial_due_date"],
                "tutorial_release_date": tut["tutorial_release_date"],
                "tutorial_answer_release_date": tut["tutorial_answer_release_date"],
                "tutorial_answer_release_date_passed": datetime.strptime(
                    tut["tutorial_answer_release_date"], "%Y-%m-%d"
                )
                <= datetime.now(),
                "course": tut["course"],
                "tutorial_questions": tut["tutorial_questions"],
                "tutorial_description": tut["tutorial_description"],
            }
            for question in tutorial_student_rec["tutorial_questions"]:
                question["rating"] = 1
                question["comment"] = ""
            db.tutorial_student.insert_one(tutorial_student_rec)
            return render_template(
                "update_record_tutorial.html",
                tutorial=tutorial_student_rec,
            )

        tutorial_student_rec["tutorial_answer_release_date_passed"] = (
            datetime.strptime(tut["tutorial_answer_release_date"], "%Y-%m-%d")
            <= datetime.now()
        )

        return render_template(
            "update_record_tutorial.html",
            tutorial=tutorial_student_rec,
        )
