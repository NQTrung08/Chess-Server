import mysql.connector
from flask import request

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


def create_product_controllers():
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        data = request.get_json()
        name = data.get("name", "")
        price = data.get("price", "")
        description = data.get("description", "")
        stock_quantity = data.get("stock_quantity", "")
        photo = data.get("photo", "")
        featured = data.get("featured", False)

        if not all([name, price, stock_quantity, photo, featured]):
            return {"message": "A fields are required"}, 400

        try:
            price = float(price)
            stock_quantity = int(stock_quantity)
        except ValueError:
            return {
                "error": "Price and stock quantity must be numeric values"
            }, 400

        if stock_quantity < 0:
            return {"error": "Stock quantity cannot be negative"}, 400

        cursor.execute(
            "INSERT INTO products (name, price, description, stock_quantity, photo, featured) VALUES (%s, %s, %s, %s, %s, %s,)",
            (name, price, description, stock_quantity, photo, featured),
        )

        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Product created successfully"}
    except mysql.connector.Error as err:
        print("Error creating product:", err)
        return None


def update_product_controllers(product_id):
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        data = request.get_json()
        name = data.get("name", "")
        price = data.get("price", "")
        description = data.get("description", "")
        stock_quantity = data.get("stock_quantity", "")
        photo = data.get("photo", "")
        featured = data.get("featured", False)

        if not all([name, price, stock_quantity, photo, featured]):
            return {"message": "A fields are required"}, 400

        try:
            price = float(price)
            stock_quantity = int(stock_quantity)
        except ValueError:
            return {
                "error": "Price and stock quantity must be numeric values"
            }, 400

        if stock_quantity < 0:
            return {"error": "Stock quantity cannot be negative"}, 400

        update_query = """
                UPDATE products
                SET name = %s, price = %s, description = %s,
                    stock_quantity = %s, photo = %s, featured = %s
                WHERE id = %s
            """
        cursor.execute(
            update_query,
            (
                name,
                price,
                description,
                stock_quantity,
                photo,
                featured,
                product_id,
            ),
        )
        connection.commit()
        cursor.execute(f"SELECT * FROM products WHERE id = {product_id}")
        update_product = cursor.fetchone()
        cursor.close()
        connection.close()

        return {
            "message": "Product updated successfully",
            "status": 200,
            "update_product": update_product,
        }

    except mysql.connector.Error as err:
        print("Error updating product:", err)
        return None


def delete_product_controller(product_id):
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM products WHERE id = {product_id}")
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Product deleted successfully"}
    except mysql.connector.Error as err:
        print("Error deleting product:", err)
        return None


def search_products_controllers():
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        data = request.get_json()
        query = data.get("name", "")
        if query.strip():
            cursor.execute(
                f"SELECT * FROM products WHERE name LIKE '%{query}%'"
            )
        else:
            cursor.execute("SELECT * FROM products")

        products = cursor.fetchall()
        cursor.close()
        connection.close()
        return products

    except mysql.connector.Error as err:
        print("Error retrieving products:", err)
        return None
