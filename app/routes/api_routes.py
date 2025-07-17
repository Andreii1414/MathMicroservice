from flask import Blueprint, jsonify, render_template
from app.controllers import math_controller

math_bp = Blueprint('math', __name__)
controller = math_controller.MathController()


@math_bp.route("/ping", methods=["GET"])
def ping():
    """
    Endpoint to check if the API is running.
    """
    return jsonify({"message": "pong"}), 200


@math_bp.route("/api/fibonacci", methods=["POST"])
def fibonacci():
    """
    Endpoint to calculate the Fibonacci number for a given input.
    """
    return controller.fibonacci()


@math_bp.route("/api/power", methods=["POST"])
def power():
    """
    Endpoint to calculate the power of a base raised to an exponent.
    """
    return controller.power()


@math_bp.route("/api/factorial", methods=["POST"])
def factorial():
    """
    Endpoint to calculate the factorial of a given input.
    """
    return controller.factorial()


@math_bp.route("/api/requests", methods=["GET"])
def get_all_requests():
    """
    Get all API request records (optional: filter by operation).
    Example: /requests?operation=fibonacci
    """
    return controller.get_requests()


@math_bp.route("/", methods=["GET"])
def index():
    """
    Render the main UI page.
    """
    return render_template("index.html")
