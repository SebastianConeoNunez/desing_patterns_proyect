from flask import Blueprint, request, jsonify
from werkzeug.exceptions import HTTPException

from src.dtos.request.favorite_request import FavoriteRequestDTO
from src.interfaces.services.favorites_service_interface import IFavoritesService

favorites_bp = Blueprint("favorites", __name__)
favorites_service: IFavoritesService = None

def set_favorites_service(service: IFavoritesService):
    global favorites_service
    favorites_service = service

@favorites_bp.get("/")
def get_favorites():
    try:
        favorites = favorites_service.get_all()
        return jsonify(favorites), 200
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500

@favorites_bp.post("/")
def create_favorite():
    try:
        payload = request.get_json()
        dto = FavoriteRequestDTO(**payload)
        new_favorite = favorites_service.create_one(dto)
        return jsonify(new_favorite), 201
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500

@favorites_bp.delete("/")
def delete_favorite():
    try:
        payload = request.get_json()
        dto = FavoriteRequestDTO(**payload)
        favorites_service.delete_one(dto)
        return '', 204
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500
