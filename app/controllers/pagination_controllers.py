import mysql.connector
from flask import jsonify, request

from app.models.database import get_database_connection


def get_poduct_paginate():
    try:
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 8, type=int)
        offset = (page - 1) * limit

        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(f"SELECT * FROM products LIMIT {limit} OFFSET {offset}")
        products = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS total FROM products")
        total_products = cursor.fetchone()["total"]
        cursor.close()
        connection.close()

        reponse = {
            "page": page,
            "limit": limit,
            "offset": offset,
            "total_products": total_products,
            "total_pages": int(total_products / limit) + 1,
            "products": products,
        }
        return reponse

    except mysql.connector.Error as err:
        print("Error retrieving products:", err)
        return None
