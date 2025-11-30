from werkzeug.exceptions import BadRequest , NotFound
from src.interfaces.repositories.categories_repository_interface import ICategoriesRepository
from src.interfaces.services.categories_service_interface import IcategoriesService
from src.dtos.request.category_request import categoryRequestDTO
from src.models.category import Category

from src.mappers.category_mapper import CategoriesMapper

class CategoriesService(IcategoriesService):
    def __init__(self, Category_repository: ICategoriesRepository):
        self.db = Category_repository
    
    def get_all(self)->list:
        """
        Method to get all Category.
        Returns:
            List of Category as dictionaries (JSON serializable)
        """
        categories:list[Category] = self.db.get_all()
  
        return [
            {
                "id": category.id,
                "name": category.name,
            }
            for category in categories
        ]
    
    def get_one_by_id(self, category_id:int)->dict:
        """
        Method to get one category by id

        Args:
            category_id (int): category identifier

        Returns:
            dict: category data as dictionary (JSON serializable)
        """
        if not category_id:
            raise BadRequest("category ID is required")
        
        category = self.db.get_one_by_id(category_id)
        if not category:
            raise NotFound(f"category with ID {category_id} not found")
        
        return {
            "id": category.id,
            "name": category.name
        }
    
    def create_one(self, category_data: categoryRequestDTO)->dict:
        """ 
        Method to create one category.

        Args:
            category_data (categoryRequestDTO): data to create category
        
        Returns:
            dict: created category as dictionary (JSON serializable)
        """
        if not category_data:
            raise BadRequest("category data is required")
        
        category:Category = CategoriesMapper.map_raw_data_to_category(category_data.model_dump())
        
        created_category = self.db.add_one(category)
        
        return {
            "id": created_category.id,
            "name": created_category.name,
        }
       
    def delete_one(self, category_data: categoryRequestDTO)->None:
        """ 
        Method to create one category.

        Args:
            category_data (categoryRequestDTO): data to create category
        
        Returns:
            dict: created category as dictionary (JSON serializable)
        """
        if not category_data:
            raise BadRequest("category data is required")
        
        category:Category = CategoriesMapper.map_raw_data_to_category(category_data.model_dump())
        
        wasDeleted = self.db.delete_one(category)

        if not wasDeleted:
            raise NotFound(f"category with ID {category.id} not found")
        
        return None


