import uuid


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
    tutorial_id = str(uuid.uuid4())
    print(f"Creating tutorial with ID: {tutorial_id}")

    # Process questions
    tutorial_questions = []
    for question in data["tutorial_questions"]:
        question_id = str(uuid.uuid4())
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
