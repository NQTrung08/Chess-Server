import mysql.connector

from app.models.database import get_database_connection


def get_products_controllers():
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
