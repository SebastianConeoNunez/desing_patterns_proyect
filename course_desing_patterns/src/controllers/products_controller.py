from flask import Blueprint, request, jsonify
from werkzeug.exceptions import HTTPException

from src.dtos.request.create_product_request import ProductCreateDTO
from src.interfaces.services.products_service_interface import IProductsService


products_bp = Blueprint("products", __name__)
products_service: IProductsService = None


def set_products_service(service: IProductsService):
    """Dependency injection for ProductsService."""
    global products_service
    products_service = service


@products_bp.get("/")
def get_products():
    """
    Retrieve all products, optionally filtered by category.

    Returns:
        JSON response with products list and HTTP status code
    """
    try:
        category = request.args.get("category") 
        all_products = products_service.get_all(category_filter=category)
        return jsonify(all_products), 200
    
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@products_bp.get("/<int:product_id>")
def get_product_by_id(product_id):
    """
    Retrieve a single product by its ID.

    Args:
        product_id: The product identifier

    Returns:
        JSON response with product data and HTTP status code
    """
    try:
        product = products_service.get_one_by_id(product_id=product_id)
        return jsonify(product), 200
    
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500



@products_bp.post("/")
def create_product():
    """
    Create a new product with the provided data.
    
    Returns:
        JSON response with created product and HTTP status code
    """
    try:
        request_payload = request.get_json()
        dto = ProductCreateDTO(**request_payload) 
        new_product = products_service.create_one(dto)
        return jsonify(new_product), 201

    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
