import json
from typing import List
from werkzeug.exceptions import BadRequest
from src.configurations.constants import FAVORITES, PRODUCTS
from src.mappers.favorite_mapper import FavoriteMapper
from src.models.favorite import Favorite
from src.interfaces.repositories.favorites_repository_interface import IFavoritesRepository
from src.interfaces.repositories.session_interface import IDatabaseConnection


class FavoritesRepository(IFavoritesRepository):

    def __init__(self, database_connection: IDatabaseConnection):
        self.db: IDatabaseConnection = database_connection

    def get_all(self) -> List[Favorite]:
        if not self.db.data:
            return []
        
        raw_favorites = self.db.data.get(FAVORITES, [])
        return list(map(FavoriteMapper.map_raw_data_to_favorite, raw_favorites))

    def add_one(self, favorite: Favorite) -> Favorite:
        if not self.db.data:
            return None
        
        favorites = self.db.data.get(FAVORITES, [])
        products = self.db.data.get(PRODUCTS, [])

        product_exists = any(p.get("id") == favorite.product_id for p in products)
        if not product_exists:
            raise BadRequest(f"Product with id {favorite.product_id} does not exist")


        for fav in favorites:
            if fav.get("user_id") == favorite.user_id and fav.get("product_id") == favorite.product_id:
                raise BadRequest("Favorite already exists for this user and product")

        favorite_dict = {
            "user_id": favorite.user_id,
            "product_id": favorite.product_id
        }

        favorites.append(favorite_dict)
        self.db.data[FAVORITES] = favorites

        with open(self.db.json_file_path, 'w') as json_file:
            json.dump(self.db.data, json_file, indent=4)

        return favorite

    def delete_one(self, favorite: Favorite) -> bool:
        if not self.db.data:
            return False

        favorites = self.db.data.get(FAVORITES, [])

        found = False
        for fav in favorites:
            if fav.get("user_id") == favorite.user_id and fav.get("product_id") == favorite.product_id:
                found = True

        if not found:
            raise BadRequest("Favorite does not exist")

        favorites = list(filter(
            lambda f: not (f.get("user_id") == favorite.user_id and f.get("product_id") == favorite.product_id),
            favorites
        ))

        self.db.data[FAVORITES] = favorites

        with open(self.db.json_file_path, 'w') as json_file:
            json.dump(self.db.data, json_file, indent=4)

        return True
