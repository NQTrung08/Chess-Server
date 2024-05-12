import mysql.connector

from config import db_config


def get_database_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        print("Database connection successful!")
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to MySQL:", err)
        return None


def get_products():
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        cursor.close()
        connection.close()
        return products
    except mysql.connector.Error as err:
        print("Error retrieving products:", err)
        return None
