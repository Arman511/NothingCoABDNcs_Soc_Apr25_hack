import uuid


def get_all_courses():
    """
    Function to get all courses.
    """
    from app import db

    courses = db.courses.find()
    return list(courses)


def get_all_courses_ids():
    """
    Function to get all courses ids.
    """
    data = get_all_courses()

    return [course["course_id"] for course in data]


def course_exists(course_id):
    """
    Function to check if a course exists.
    """
    from app import db

    course = db.courses.find_one({"course_id": course_id})
    if course:
        return True

    return False


def add_course(course):
    """
    Function to add a course.
    """
    from app import db

    # Check if the course already exists
    if db.courses.find_one({"course_id": course["course_id"]}):
        return {"error": "Course already exists"}, 400

    # Add the course to the database
    course["_id"] = uuid.uuid1().hex
    db.courses.insert_one(course)
    return {"message": "Course added successfully"}, 201
