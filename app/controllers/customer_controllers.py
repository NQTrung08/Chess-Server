import mysql.connector
from flask import jsonify, request
from flask_bcrypt import Bcrypt
from mysql.connector import Error

from app.models.database import get_database_connection

bcrypt = Bcrypt()


def register():
    data = request.get_json()

    # Validate incoming data
    if not all(key in data for key in ("name", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    name = data["name"]
    email = data["email"]
    password = data["password"]
    address = data.get("address", "")
    role = data.get("role", "user")
    provider_id = data.get("provider_id", "")
    provider = data.get("provider", "")

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    connection = get_database_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT email FROM customers WHERE email = %s", (email,)
        )
        if cursor.fetchone():
            return jsonify({"error": "Email already exists"}), 409

        # Insert the new user into the database
        insert_query = """
        INSERT INTO customers (name, email, password, address, role, provider_id, provider)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_query,
            (
                name,
                email,
                hashed_password,
                address,
                role,
                provider_id,
                provider,
            ),
        )
        connection.commit()

        cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
        user = cursor.fetchone()

        return (
            jsonify({"message": "User registered successfully", "data": user}),
            200,
        )
    except Error as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()


def login():
    data = request.get_json()

    if not all(key in data for key in ("email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    email = data["email"]
    password = data["password"]

    connection = get_database_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user["password"], password):
            return jsonify({"message": "Login successful", "data": user}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()
