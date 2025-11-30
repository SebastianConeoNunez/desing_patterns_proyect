from typing import Any, Dict
from src.models.category import Category
from src.models.category import Category


class CategoriesMapper:
    @staticmethod
    def map_raw_data_to_category(raw_category: Dict[str, Any]) -> Category:
        """
        Maps a raw dictionary to a Category object using the Builder pattern.
        
        Args:
            raw_Category: Dictionary containing Category data
            
        Returns:
            Category object built and validated
            
        Raises:
            ValueError: If the data is invalid
        """
        return (Category()
            .set_id(raw_category.get('id'))
            .set_name(raw_category.get('name'))
            .build())