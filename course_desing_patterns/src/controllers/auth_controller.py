from flask import Blueprint, request, jsonify
from werkzeug.exceptions import HTTPException

from src.dtos.request.register_request import RegisterRequestDTO
from src.dtos.request.login_request import LoginRequestDTO
from src.interfaces.services.auth_service_interface import IAuthService


auth_bp = Blueprint("auth", __name__)
auth_service: IAuthService = None


def set_auth_service(service: IAuthService):
    """Dependency injection for AuthService."""
    global auth_service
    auth_service = service


@auth_bp.post("/register")
def register():
    """
    Register a new user in the system.

    Request Body:
        email: User email (unique)
        password: User password (min 8 characters)
        name: User full name

    Returns:
        JSON response with user data and HTTP status code 201
    """
    try:
        payload = request.get_json()
        dto = RegisterRequestDTO(**payload)
        new_user = auth_service.register(dto)
        return jsonify(new_user), 201
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.post("/login")
def login():
    """
    Authenticate a user and generate JWT token.

    Request Body:
        email: User email
        password: User password

    Returns:
        JSON response with token and user data and HTTP status code 200
    """
    try:
        payload = request.get_json()
        dto = LoginRequestDTO(**payload)
        result = auth_service.login(dto)
        return jsonify(result), 200
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500