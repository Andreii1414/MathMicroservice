from flask import Blueprint, jsonify, render_template
from app.controllers import math_controller

controller = math_controller.MathController()

def register_routes(app):
    @app.route("/ping", methods=["GET"])
    def ping():
        """
        Endpoint to check if the API is running.
        """
        return jsonify({"message": "pong"}), 200


    @app.route("/api/fibonacci", methods=["POST"])
    def fibonacci():
        """
        Endpoint to calculate the Fibonacci number for a given input.
        """
        return controller.fibonacci()


    @app.route("/api/power", methods=["POST"])
    def power():
        """
        Endpoint to calculate the power of a base raised to an exponent.
        """
        return controller.power()


    @app.route("/api/factorial", methods=["POST"])
    def factorial():
        """
        Endpoint to calculate the factorial of a given input.
        """
        return controller.factorial()


    @app.route("/api/requests", methods=["GET"])
    def get_all_requests():
        """
        Get all API request records (optional: filter by operation).
        Example: /requests?operation=fibonacci
        """
        return controller.get_requests()


    @app.route("/", methods=["GET"])
    def index():
        """
        Render the main UI page.
        """
        return render_template("index.html")


    @app.route("/api/logs", methods=["GET"])
    def get_logs():
        """
        Endpoint to retrieve logs from the database.
        """
        return controller.get_logs()
