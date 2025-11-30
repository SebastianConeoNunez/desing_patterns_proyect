from abc import ABC, abstractmethod


class IcategoriesService(ABC):
    
    @abstractmethod
    def get_all(self)->list:
        """Retrieve all categorys"""
   
    @abstractmethod
    def create_one(self, category_data)->dict:
        """Create a new category with the provided data."""
    
    @abstractmethod
    def get_one_by_id(self, category_id)->dict:
        """Retrieve a single category by its ID."""


    @abstractmethod
    def delete_one(self, category_data)->dict:
        """Delete category with provided data."""
