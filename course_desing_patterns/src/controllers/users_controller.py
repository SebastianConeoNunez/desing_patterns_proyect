from flask import Blueprint, request, jsonify
from werkzeug.exceptions import HTTPException

from src.dtos.request.update_user_request import UpdateUserRequestDTO
from src.interfaces.services.users_service_interface import IUsersService


users_bp = Blueprint("users", __name__)
users_service: IUsersService = None


def set_users_service(service: IUsersService):
    """Dependency injection for UsersService."""
    global users_service
    users_service = service


@users_bp.get("/")
def get_users():
    """
    Retrieve all users (admin only).

    Returns:
        JSON response with users list and HTTP status code 200
    """
    try:
        # TODO: Add @require_role(ADMIN) middleware
        all_users = users_service.get_all()
        return jsonify(all_users), 200
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@users_bp.get("/<int:user_id>")
def get_user_by_id(user_id):
    """
    Retrieve a single user by its ID.

    Args:
        user_id: The user identifier

    Returns:
        JSON response with user data and HTTP status code 200
    """
    try:
        user = users_service.get_by_id(user_id=user_id)
        return jsonify(user), 200
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@users_bp.put("/<int:user_id>")
def update_user(user_id):
    """
    Update user information.

    Args:
        user_id: The user identifier

    Request Body:
        name: Updated user name (optional)
        password: Updated password (optional)

    Returns:
        JSON response with updated user data and HTTP status code 200
    """
    try:
        payload = request.get_json()
        dto = UpdateUserRequestDTO(**payload)
        updated_user = users_service.update_one(user_id=user_id, update_dto=dto)
        return jsonify(updated_user), 200
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@users_bp.delete("/<int:user_id>")
def delete_user(user_id):
    """
    Delete (deactivate) a user account.

    Args:
        user_id: The user identifier

    Returns:
        Empty response with HTTP status code 204
    """
    try:
        users_service.delete_one(user_id=user_id)
        return '', 204
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
