import mysql.connector
from flask import jsonify, request

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
        # Use parameterized query to prevent SQL injection
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()  # Fetch one product, assuming id is unique
        cursor.close()
        connection.close()
        return product
    except Exception as e:
        # You may want to log the error or raise a custom exception
        print(f"An error occurred: {e}")
        return None


def create_product_controllers():
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        data = request.get_json()

        name = data.get("name", "").strip()
        price = data.get("price", "")
        discount = data.get("discount", "")
        description = data.get("description", "").strip()
        stock_quantity = data.get("stock_quantity", "")
        photo = data.get("photo", "").strip()
        featured = data.get("featured", False)

        if not name or not price or not stock_quantity:
            return (
                jsonify(
                    {"message": "Name, price, and stock quantity are required"}
                ),
                400,
            )

        try:
            price = float(price)
            discount = int(discount)
            stock_quantity = int(stock_quantity)
        except ValueError:
            return {
                "error": "Price and stock quantity must be numeric values"
            }, 400

        if stock_quantity < 0:
            return {"error": "Stock quantity cannot be negative"}, 400

        cursor.execute(
            "INSERT INTO products (name, price, discount, description, stock_quantity, photo, featured) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                name,
                price,
                discount,
                description,
                stock_quantity,
                photo,
                featured,
            ),
        )

        connection.commit()

        # cursor.execute("SELECT * FROM products WHERE name = %s", (name,))
        # product = cursor.fetchone()

        cursor.close()
        connection.close()
        # return {"message": "Product created successfully", "product": product}
        return {"message": "Product created successfully"}
    except mysql.connector.Error as err:
        print("Error creating product:", err)
        return {"message": "Error creating product"}, 500


def update_product_controllers(product_id):
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        data = request.get_json()

        name = data.get("name", "").strip()
        price = data.get("price")
        discount = data.get("discount")
        description = data.get("description", "").strip()
        stock_quantity = data["stock_quantity"]
        photo = data.get("photo", "").strip()
        featured = data.get("featured", False)

        if name == "" or price == "" or stock_quantity == "":
            return {
                "message": "Name, price, and stock quantity are required"
            }, 400

        try:
            price = float(price)
            discount = float(discount)
            stock_quantity = int(stock_quantity)
        except ValueError:
            return {
                "error": "Price and stock quantity must be numeric values"
            }, 400

        if stock_quantity < 0:
            return {"error": "Stock quantity cannot be negative"}, 400

        update_query = """
            UPDATE products
            SET name = %s, price = %s, discount = %s, description = %s,
                stock_quantity = %s, photo = %s, featured = %s
            WHERE id = %s
        """
        cursor.execute(
            update_query,
            (
                name,
                price,
                discount,
                description,
                stock_quantity,
                photo,
                featured,
                product_id,
            ),
        )
        connection.commit()
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        updated_product = cursor.fetchone()
        cursor.close()
        connection.close()

        return {
            "message": "Product updated successfully",
            "status": 200,
            "updated_product": updated_product,
        }
    except mysql.connector.Error as err:
        print("Error updating product:", err)
        return {"message": "Error updating product"}, 500


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
