from abc import ABC, abstractmethod
from src.dtos.request.favorite_request import FavoriteRequestDTO

class IFavoritesService(ABC):

    @abstractmethod
    def get_all(self) -> list:
        """Retrieve all favorites"""

    @abstractmethod
    def create_one(self, favorite_data: FavoriteRequestDTO) -> dict:
        """Create a new favorite with the provided data."""

    @abstractmethod
    def delete_one(self, favorite_data: FavoriteRequestDTO) -> None:
        """Delete a favorite with the provided data."""
