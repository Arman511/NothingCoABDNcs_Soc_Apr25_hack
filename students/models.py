import uuid
from flask import Flask, jsonify, redirect, render_template, request, session
from pymongo import MongoClient
import os
from passlib.hash import pbkdf2_sha512


class Student:
    """Student Class"""

    def add_student(self, student):
        """Add a student to the database"""

        from app import db

        if db.students_collection.find_one({"username": student["email"]}):
            return jsonify({"error": "Student already exists"}), 400

        # Hash the password and save the student
        hashed_password = pbkdf2_sha512.hash(student["password"])
        db.students_collection.insert_one(
            {"_id": uuid.uuid1().hex, "email": student["email"], "password": hashed_password}
        )

        return jsonify({"message": "Student added successfully"}), 201
