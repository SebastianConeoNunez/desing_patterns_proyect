from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.category import Category


class ICategoriesRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Category]:
        """Retrieve all categories"""
    
    @abstractmethod
    def get_one_by_id(self, cateogry_id: int) -> Optional[Category]:
        """Retrieve a single cateogry by its ID."""  

    @abstractmethod
    def add_one(self, category_data: Category) -> Category:
        """Add a new category with the provided data."""

    @abstractmethod
    def delete_one(self, category_data: Category) -> bool:
        """Delete a new category with the provided data."""