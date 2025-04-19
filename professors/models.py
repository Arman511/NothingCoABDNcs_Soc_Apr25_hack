import uuid
from flask import jsonify
from passlib.hash import pbkdf2_sha512


class Professor:
    """Professor Class"""

    def register_professor(self, professor):
        """Add a student to the database"""

        from app import db

        # Check if the professor already exists
        if db.professors_collection.find_one({"email": professor["email"]}):
            return jsonify({"error": "Professor already exists"}), 400

        # Hash the password and save the professor
        hashed_password = pbkdf2_sha512.hash(professor["password"])
        db.professors_collection.insert_one(
            {
                "_id": uuid.uuid1().hex,
                "email": professor["email"],
                "password": hashed_password,
            }
        )

        return jsonify({"message": "Professor added successfully"}), 201
