# from flask import Blueprint, request, jsonify
# from werkzeug.exceptions import HTTPException

# from src.dtos.request.create_product_request import ProductCreateDTO
# from src.interfaces.services.products_service_interface import IProductsService


# categorys_bp = Blueprint("categorys", __name__)
# categorys_service: IcategorysService = None


# def set_categorys_service(service: IcategorysService):
#     """Dependency injection for categorysService."""
#     global categorys_service
#     categorys_service = service


# @categorys_bp.get("/")
# def get_categorys():
#     """
#     Retrieve all categorys, optionally filtered by category.

#     Returns:
#         JSON response with categorys list and HTTP status code
#     """
#     try:
#         category = request.args.get("category") 
#         all_categorys = categorys_service.get_all(category_filter=category)
#         return jsonify(all_products), 200
    
#     except HTTPException as e:
#         return jsonify({"error": e.description}), e.code
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"error": "Internal server error"}), 500


# @products_bp.get("/<int:product_id>")
# def get_product_by_id(product_id):
#     """
#     Retrieve a single product by its ID.

#     Args:
#         product_id: The product identifier

#     Returns:
#         JSON response with product data and HTTP status code
#     """
#     try:
#         product = products_service.get_one_by_id(product_id=product_id)
#         return jsonify(product), 200
    
#     except HTTPException as e:
#         return jsonify({"error": e.description}), e.code
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"error": "Internal server error"}), 500



# @products_bp.post("/")
# def create_product():
#     """
#     Create a new product with the provided data.
    
#     Returns:
#         JSON response with created product and HTTP status code
#     """
#     try:
#         request_payload = request.get_json()
#         dto = ProductCreateDTO(**request_payload) 
#         new_product = products_service.create_one(dto)
#         return jsonify(new_product), 201

#     except HTTPException as e:
#         return jsonify({"error": e.description}), e.code
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"error": "Internal server error"}), 500
