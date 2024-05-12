from flask import Flask, jsonify

from app.models.database import get_database_connection, get_products

app = Flask(__name__)


connect_database = get_database_connection()


@app.route("/products")
def get_all_products():
    product = get_products()
    return jsonify(product)


if __name__ == "__main__":
    app.run(debug=True)
