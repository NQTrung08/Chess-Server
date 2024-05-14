from flask import Flask, jsonify

from app.controllers.pagination_controllers import get_poduct_paginate
from app.controllers.product_controllers import (
    get_product_controllers,
    get_products_controllers,
)


def init_app():
    app = Flask(__name__)

    @app.route("/products", methods=["GET"])
    def get_all_products():
        products = get_products_controllers()
        return jsonify({"products": products})

    @app.route("/product/<int:product_id>", methods=["GET"])
    def get_product(product_id):
        product = get_product_controllers(product_id)
        return jsonify({"product": product})

    @app.route("/sale", methods=["GET"])
    def get_paginate():
        products = get_poduct_paginate()
        return jsonify(products)

    return app
