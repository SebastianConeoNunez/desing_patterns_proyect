from werkzeug.exceptions import BadRequest, NotFound
from src.interfaces.repositories.favorites_repository_interface import IFavoritesRepository
from src.interfaces.services.favorites_service_interface import IFavoritesService
from src.dtos.request.favorite_request import FavoriteRequestDTO
from src.models.favorite import Favorite
from src.mappers.favorite_mapper import FavoriteMapper

class FavoritesService(IFavoritesService):

    def __init__(self, favorites_repository: IFavoritesRepository):
        self.db = favorites_repository

    def get_all(self) -> list:
        favorites = self.db.get_all()
        return [
            {
                "user_id": fav.user_id,
                "product_id": fav.product_id
            } for fav in favorites
        ]

    def create_one(self, favorite_data: FavoriteRequestDTO) -> dict:
        if not favorite_data:
            raise BadRequest("Favorite data is required")

        favorite: Favorite = FavoriteMapper.map_raw_data_to_favorite(favorite_data.model_dump())
        created_favorite = self.db.add_one(favorite)

        return {
            "user_id": created_favorite.user_id,
            "product_id": created_favorite.product_id
        }

    def delete_one(self, favorite_data: FavoriteRequestDTO) -> None:
        if not favorite_data:
            raise BadRequest("Favorite data is required")

        favorite: Favorite = FavoriteMapper.map_raw_data_to_favorite(favorite_data.model_dump())
        deleted = self.db.delete_one(favorite)

        if not deleted:
            raise NotFound("Favorite not found")

        return None
