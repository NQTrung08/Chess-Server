import mysql.connector

from app.models.database import get_database_connection


def get_products_controllers():
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        connection.close()
        return products
    except mysql.connector.Error as err:
        print("Error retrieving products:", err)
        return None


def get_product_controllers(product_id):
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = {product_id}")
        product_id = cursor.fetchall()
        cursor.close()
        connection.close()
        return product_id
    except mysql.connector.Error as err:
        print("Error retrieving products:", err)
        return None
