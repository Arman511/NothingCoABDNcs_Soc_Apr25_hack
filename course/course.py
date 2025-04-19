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
