import uuid
from flask import jsonify, session
from passlib.hash import pbkdf2_sha512


class Student:
    """Student Class"""

    def add_student(self, student):
        """Add a student to the database"""

        from app import db

        if db.students.find_one({"username": student["email"]}):
            return jsonify({"error": "Student already exists"}), 400

        # Hash the password and save the student
        hashed_password = pbkdf2_sha512.hash(student["password"])
        db.students.insert_one(
            {
                "_id": uuid.uuid1().hex,
                "email": student["email"],
                "password": hashed_password,
            }
        )

        return jsonify({"message": "Student added successfully"}), 201

    def get_student_by_email(self, student):

        from app import db

        student = db.students.find_one({"email": student["email"]})
        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({"message": "Student found successfully"}), 200

    def get_students(self):
        """Get all students from the database"""

        from app import db

        students = db.students.find()
        if not students:
            return jsonify({"error": "No students found"}), 404

        return jsonify({"students": list(students)}), 200

    def delete_student(self, student):
        """Delete a student from the database"""

        from app import db

        if not db.students.find_one({"email": student["email"]}):
            return jsonify({"error": "Student not found"}), 404

        db.students.delete_one({"email": student["email"]})

        return jsonify({"message": "Student deleted successfully"}), 200

    def update_student_course_info(self, courses):
        """Update a student in the database"""

        from app import db

        student_uuid = session.get("student")

        if not db.students.find_one({"_id": student_uuid}):
            return jsonify({"error": "Student not found"}), 404

        db.students.update_one(
            {"_id": student_uuid},
            {
                "$set": {
                    "courses": courses,
                }
            },
        )

        return jsonify({"message": "Student updated successfully"}), 200

    def get_student_by_uuid(self, student_uuid):
        """Get a student by UUID from the database"""

        from app import db

        student = db.students.find_one({"_id": student_uuid})
        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return student
