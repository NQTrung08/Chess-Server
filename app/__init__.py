from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from app.chat_controllers import get_response
from app.controllers.customer_controllers import (
    get_customers_controllers,
    login,
    register,
)
from app.controllers.pagination_controllers import get_poduct_paginate
from app.controllers.product_controllers import (
    create_product_controllers,
    delete_product_controller,
    get_product_controllers,
    get_products_controllers,
    search_products_controllers,
    update_product_controllers,
)
from app.models.database import get_database_connection


def init_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/products", methods=["GET"])
    def get_all_products():
        products = get_products_controllers()
        return jsonify(products)

    @app.route("/product/<int:product_id>", methods=["GET"])
    def get_product(product_id):
        product = get_product_controllers(product_id)
        return jsonify(product)

    @app.route("/cproduct", methods=["POST"])
    def create_product():
        product = create_product_controllers()
        return product

    @app.route("/uproduct/<int:product_id>", methods=["PUT"])
    def update_product(product_id):
        product = update_product_controllers(product_id)
        return product

    @app.route("/dproduct/<int:product_id>", methods=["DELETE"])
    def delete_product(product_id):
        product = delete_product_controller(product_id)
        return jsonify(product)

    @app.route("/sale", methods=["GET"])
    def get_paginate():
        products = get_poduct_paginate()
        return jsonify(products)

    @app.route("/products/search", methods=["POST"])
    def search_products():
        products = search_products_controllers()
        return jsonify(products)

    @app.route("/register", methods=["POST"])
    def register_user():
        user = register()
        return user

    @app.route("/login", methods=["POST"])
    def login_user():
        user = login()
        return user

    @app.route("/customers", methods=["GET"])
    def get_customers():
        customers = get_customers_controllers()
        return jsonify(customers)

    @app.route("/predict", methods=["POST"])
    def chatbot():
        response = get_response()
        return jsonify({"response": response})

    return app
