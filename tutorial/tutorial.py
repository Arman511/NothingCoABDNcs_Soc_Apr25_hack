import uuid

from flask import session


def make_tutorial(data):
    """
    Function to create a tutorial.
    """

    from app import db

    required_fields = [
        "course",
        "tutorial_name",
        "tutorial_release_date",
        "tutorial_due_date",
        "tutorial_description",
        "tutorial_answer_release_date",
        "tutorial_questions",
    ]

    # Validate required fields
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"'{field}' is required but not found in data.")

    # Generate a unique tutorial ID
    tutorial_id = str(uuid.uuid4().hex)
    print(f"Creating tutorial with ID: {tutorial_id}")

    # Process questions
    tutorial_questions = []
    for question in data["tutorial_questions"]:
        question_id = str(uuid.uuid4().hex)
        question["_id"] = question_id
        tutorial_questions.append(question)
        print(f"Added question with ID: {question_id}")

    # Sort questions by their question number
    tutorial_questions.sort(key=lambda x: x["custom_id"])

    # Check if the course exists
    course_id = data["course"]
    from course import course

    if not course.course_exists(course_id):
        print(f"Course with ID '{course_id}' does not exist.")
        raise ValueError(f"Course with ID '{course_id}' does not exist.")

    # Check if dates are valid

    if data["tutorial_release_date"] > data["tutorial_due_date"]:
        print("Release date cannot be after due date.")
        raise ValueError("Release date cannot be after due date.")
    if data["tutorial_due_date"] > data["tutorial_answer_release_date"]:
        print("Due date cannot be after answer release date.")
        raise ValueError("Due date cannot be after answer release date.")
    if data["tutorial_answer_release_date"] < data["tutorial_release_date"]:
        print("Answer release date cannot be before release date.")
        raise ValueError("Answer release date cannot be before release date.")

    # Construct the tutorial object
    tutorial = {
        "_id": tutorial_id,
        "course": data["course"],
        "tutorial_name": data["tutorial_name"],
        "tutorial_release_date": data["tutorial_release_date"],
        "tutorial_due_date": data["tutorial_due_date"],
        "tutorial_description": data["tutorial_description"],
        "tutorial_answer_release_date": data["tutorial_answer_release_date"],
        "tutorial_questions": tutorial_questions,
    }

    # Save the tutorial to the database
    try:
        db.tutorials.insert_one(tutorial)
        print("Tutorial created successfully.")
    except Exception as e:
        print(f"Failed to create tutorial: {e}")
        raise RuntimeError("Database operation failed.") from e

    return tutorial_id


def get_tutorial_by_uuid(tutorial_uuid):
    """
    Function to get a tutorial by its UUID.
    """

    from app import db

    tutorial = db.tutorials.find_one({"_id": tutorial_uuid})
    if not tutorial:
        print(f"Tutorial with ID '{tutorial_uuid}' not found.")
        raise ValueError(f"Tutorial with ID '{tutorial_uuid}' not found.")
    return tutorial


def get_all_tutorials():
    """
    Function to get all tutorials.
    """
    from app import db

    tutorials = db.tutorials.find()
    if not tutorials:
        print("No tutorials found.")
        return []
    return list(tutorials)


def update_student_tutorial(data, tutorial_uuid):
    """
    Function to update a student's tutorial record.
    """

    from app import db

    # Validate required fields
    if not data or not tutorial_uuid:
        print("No data provided.")
        raise ValueError("No data provided.")

    rating = data.get("ratings")
    comments = data.get("comments")

    if not rating:
        print("Rating is required.")
        return (
            {"error": "Rating is required."},
            400,
        )

    tutorial_rec = db.tutorial_student.find_one(
        {"tutorial_id": tutorial_uuid, "student_id": session.get("student")}
    )
    if not tutorial_rec:
        print("No tutorial record found.")
        return (
            {"error": "No tutorial record found."},
            404,
        )

    for question in tutorial_rec["tutorial_questions"]:
        question["rating"] = rating[question["custom_id"]]
        question["comment"] = comments[question["custom_id"]].strip()

    db.tutorial_student.update_one(
        {"tutorial_id": tutorial_uuid, "student_id": session.get("student")},
        {
            "$set": {
                "tutorial_questions": tutorial_rec["tutorial_questions"],
            }
        },
    )

    return (
        {"message": "Tutorial record updated successfully."},
        200,
    )
