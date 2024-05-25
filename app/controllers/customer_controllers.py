import mysql.connector
from flask import jsonify, request
from flask_bcrypt import Bcrypt
from mysql.connector import Error

from app.models.database import get_database_connection

bcrypt = Bcrypt()

# Hàm đăng ký người dùng
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

        return jsonify({"message": "User registered successfully"}), 200
    except Error as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Hàm đăng nhập người dùng
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

# Hàm lấy danh sách tất cả khách hàng
def get_all_customers():
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, role FROM customers")
        customers = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(customers), 200
    except Error as e:
        print("Error retrieving customers:", e)
        return jsonify({"error": str(e)}), 500

# Hàm lấy thông tin một khách hàng
def get_customer(user_id):
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, role FROM customers WHERE id = %s", (user_id,))
        customer = cursor.fetchone()
        cursor.close()
        connection.close()
        return jsonify(customer), 200 if customer else 404
    except Error as e:
        print("Error retrieving customer:", e)
        return jsonify({"error": str(e)}), 500


