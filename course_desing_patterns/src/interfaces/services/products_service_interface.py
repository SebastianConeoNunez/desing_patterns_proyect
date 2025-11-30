from abc import ABC, abstractmethod


class IProductsService(ABC):
    
    @abstractmethod
    def get_all(self, category_filter=None)->list:
        """Retrieve all products, optionally filtered by category."""
   
    @abstractmethod
    def get_one_by_id(self, product_id)->dict:
        """Retrieve a single product by its ID."""

    @abstractmethod
    def create_one(self, product_data)->dict:
        """Create a new product with the provided data."""
