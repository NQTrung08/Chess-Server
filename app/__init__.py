from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from app.controllers.customer_controllers import (
    login, 
    register, 
    get_all_customers, 
    get_customer
)
from app.controllers.pagination_controllers import get_poduct_paginate
from app.controllers.product_controllers import (
    create_product_controllers,
    delete_product_controller,
    get_product_controllers,
    get_products_controllers,
    search_products_controllers,
    update_product_controllers,
    update_discount_controller,
    get_discount_controller
)
from app.models.database import get_database_connection


def init_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/", methods=["GET"])
    def get_hello():
        return jsonify("hello world")

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
        return jsonify(product)

    @app.route("/uproduct/<int:product_id>", methods=["PUT"])
    def update_product(product_id):
        product = update_product_controllers(product_id)
        return jsonify(product)

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

    # Các route mới cho quản lý khách hàng
    @app.route("/customers", methods=["GET"])
    def get_customers():
        return get_all_customers()

    @app.route("/customer/<int:user_id>", methods=["GET"])
    def get_customer_detail(user_id):
        return get_customer(user_id)
    
     # Các route mới cho quản lý discount
    @app.route("/product/<int:product_id>/discount", methods=["PUT"])
    def update_discount(product_id):
        data = request.get_json()
        discount = data.get('discount')
        response = update_discount_controller(product_id, discount)
        return jsonify(response)

    @app.route("/product/<int:product_id>/discount", methods=["GET"])
    def get_discount(product_id):
        response = get_discount_controller(product_id)
        return jsonify(response)
    
    return app


app = init_app()

if __name__ == "__main__":
    app.run(debug=True)