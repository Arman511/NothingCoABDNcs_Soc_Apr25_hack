import uuid


def make_tutorial(data):
    from app import db

    """
    Function to create a tutorial.
    """
    print("Creating a tutorial...")

    course = data.get("course")
    if not course:
        raise ValueError("Course not found in data.")
    print(f"Course: {course}")
    tutorial_name = data.get("tutorial_name")
    if not tutorial_name:
        raise ValueError("Tutorial name not found in data.")

    tutorial_release_date = data.get("tutorial_release_date")
    if not tutorial_release_date:
        raise ValueError("Tutorial release date not found in data.")

    tutorial_due_date = data.get("tutorial_due_date")
    if not tutorial_due_date:
        raise ValueError("Tutorial due date not found in data.")

    tutorial_description = data.get("tutorial_description")
    if not tutorial_description:
        raise ValueError("Tutorial description not found in data.")
    tutorial_id = str(uuid.uuid4())
    print(f"Tutorial ID: {tutorial_id}")

    tutorial_answer_release_date = data.get("tutorial_answer_release_date")
    if not tutorial_answer_release_date:
        raise ValueError("Tutorial answer release date not found in data.")

    tutorial_questions = data.get("tutorial_questions")

    for question in tutorial_questions:
        question_id = str(uuid.uuid4())
        question["question_id"] = question_id
        print(f"Question ID: {question_id}")

    tutorial = {
        "_id": tutorial_id,
        "course": course,
        "tutorial_name": tutorial_name,
        "tutorial_release_date": tutorial_release_date,
        "tutorial_due_date": tutorial_due_date,
        "tutorial_description": tutorial_description,
        "tutorial_answer_release_date": tutorial_answer_release_date,
        "tutorial_questions": tutorial_questions,
    }

    # Save the tutorial to the database

    db.tutorials.insert_one(tutorial)
    print("Tutorial created successfully.")
    return tutorial_id
