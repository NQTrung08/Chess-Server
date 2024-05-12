from flask import Flask, jsonify

from app.models.database import get_database_connection, get_products

app = Flask(__name__)


connect_database = get_database_connection()


if __name__ == "__main__":
    app.run(debug=True)
