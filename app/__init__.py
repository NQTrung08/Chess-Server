from flask import Flask, jsonify

from app.controllers.product_controllers import get_products_controllers
from app.models.database import get_database_connection


def init_app():
    app = Flask(__name__)

    @app.route("/products")
    def get_all_products():
        products = get_products_controllers()
        return jsonify(products)

    return app
