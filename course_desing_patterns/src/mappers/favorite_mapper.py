from typing import Any, Dict
from src.models.favorite import Favorite

class FavoriteMapper:
    @staticmethod
    def map_raw_data_to_favorite(raw_favorite: Dict[str, Any]) -> Favorite:
        """
        Maps a raw dictionary to a Favorite object using the Builder style.

        Args:
            raw_favorite (dict): Dictionary containing favorite data

        Returns:
            Favorite: Favorite object built and validated

        Raises:
            ValueError: If the data is incomplete or invalid
        """
        return (
            Favorite()
            .set_user_id(raw_favorite.get("user_id"))
            .set_product_id(raw_favorite.get("product_id"))
            .build()
        )
