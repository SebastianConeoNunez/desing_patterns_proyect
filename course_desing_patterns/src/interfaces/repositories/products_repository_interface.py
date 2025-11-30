from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.product import Product


class IProductsRepository(ABC):
    @abstractmethod
    def get_all(self, category_filter: Optional[str] = None) -> List[Product]:
        """Retrieve all products, optionally filtered by category."""

    @abstractmethod
    def get_one_by_id(self, product_id: int) -> Optional[Product]:
        """Retrieve a single product by its ID."""  

    @abstractmethod
    def add_one(self, product_data: Product) -> Product:
        """Add a new product with the provided data."""