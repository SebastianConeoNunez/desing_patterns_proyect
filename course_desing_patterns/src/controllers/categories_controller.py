from flask import Blueprint, request, jsonify
from werkzeug.exceptions import HTTPException

from src.dtos.request.category_request import categoryRequestDTO
from src.interfaces.services.categories_service_interface import IcategoriesService



categories_bp = Blueprint("categorys", __name__)
categories_service: IcategoriesService = None


def set_categories_service(service: IcategoriesService):
    """Dependency injection for categoriesService."""
    global categories_service
    categories_service = service


@categories_bp.get("/")
def get_categorys():
    """
    Retrieve all categories, optionally filtered by category.

    Returns:
        JSON response with categories list and HTTP status code
    """
    try:
        all_categories = categories_service.get_all()
        return jsonify(all_categories), 200
    
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@categories_bp.get("/<int:category_id>")
def get_category_by_id(category_id):
    """
    Retrieve a single category by its ID.

    Args:
        category_id: The category identifier

    Returns:
        JSON response with category data and HTTP status code
    """
    try:
        category = categories_service.get_one_by_id(category_id=category_id)
        return jsonify(category), 200
    
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@categories_bp.post("/")
def create_category():
    """
    Create a new category with the provided data.
    
    Returns:
        JSON response with created category and HTTP status code
    """
    try:
        request_payload = request.get_json()
        dto = categoryRequestDTO(**request_payload) 
        new_category = categories_service.create_one(dto)
        return jsonify(new_category), 201

    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@categories_bp.delete("/")
def delete_category():
    """
    Delete a category.
    
    Returns:
        204 No Content if deleted successfully
    """
    try:
        request_payload = request.get_json()
        dto = categoryRequestDTO(**request_payload) 
        categories_service.delete_one(dto)
        return '', 204  #

    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500