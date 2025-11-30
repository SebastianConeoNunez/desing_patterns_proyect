import json
from typing import List
from werkzeug.exceptions import BadRequest
from src.configurations.constants import CATEGORIES
from src.mappers.category_mapper import CategoriesMapper
from src.models.category import Category
from src.interfaces.repositories.categories_repository_interface import ICategoriesRepository
from src.interfaces.repositories.session_interface import IDatabaseConnection



class CategoriesRepository(ICategoriesRepository):

    def __init__(self, database_connection: IDatabaseConnection):
        """
        Initializes the CategoriesRepository.
        
        Args:
            database_connection: Database connection instance
        """
        self.db: IDatabaseConnection = database_connection
    
    def get_all(self) -> List[Category]:
        """
        Retrieves all categorys and maps them to category objects.
        
        Args:
            category_filter: Optional category to filter categorys
        
        Returns:
            List of mapped categorys, or empty list if no data exists
        """
        if self.db.data:
            raw_categories = self.db.data.get(CATEGORIES, [])
            categories = list(map(CategoriesMapper.map_raw_data_to_category, raw_categories))
               
            return categories
        
        return []
    
    def get_one_by_id(self, category_id: int) -> Category:
        """
        Retrieves a single category by its ID.
        
        Args:
            category_id: The category identifier
            
        Returns:
            category object if found, None otherwise
        """
        if self.db.data:
            raw_categories = self.db.data.get(CATEGORIES, [])
            for raw_category in raw_categories:
                if raw_category.get('id') == category_id:
                    return CategoriesMapper.map_raw_data_to_category(raw_category)
        
        return None

    def add_one(self, category: Category) -> Category:
        """
        Adds a new Category to the database.
        
        Args:
            category: Category object to add
            
        Returns:
            The added Category with ID
            
        Raises:
            ValueError: If Category does not exist
        """
        if not self.db.data:
            return None
        
        categories = self.db.data.get('categories', [])

        category_names = [cat.get('name') for cat in categories]
        if category.name in category_names:
            raise BadRequest(f"Category '{category.name}' exist")
        
        new_id = max([p.get('id', 0) for p in categories], default=0) + 1
        category.id = new_id
        
        category_dict = {
            'id': category.id,
            'name': category.name,
        }
        
        categories.append(category_dict)
        self.db.data[CATEGORIES] = categories      

        with open(self.db.json_file_path, 'w') as json_file:
            json.dump(self.db.data, json_file, indent=4)  
        
        return category
    
    def delete_one(self, category: Category) -> bool:
        """
        Delete a new Category to the database.
        
        Args:
            category: Category object to delete
            
        Raises:
            ValueError: If Category does not exist
        """
        if not self.db.data:
            return False
        
        categories = self.db.data.get('categories', [])
        
        category_names = [cat.get('name') for cat in categories]
        if category.name not in category_names:
            raise BadRequest(f"Category '{category.name}' doesnt exist")

        categories = list(filter(lambda cat: cat.get('name') != category.name, categories))
        self.db.data['categories'] = categories

        with open(self.db.json_file_path, 'w') as json_file:
                json.dump(self.db.data, json_file, indent=4)
        
        return True