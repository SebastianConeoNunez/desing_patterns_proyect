from abc import ABC, abstractmethod
from typing import List
from src.models.favorite import Favorite

class IFavoritesRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Favorite]:
        """Retrieve all favorites"""

    @abstractmethod
    def add_one(self, favorite: Favorite) -> Favorite:
        """Add a new favorite with the provided data."""

    @abstractmethod
    def delete_one(self, favorite: Favorite) -> bool:
        """Delete a favorite with the provided data."""
