from typing import Any, Dict
from src.models.product import Product


class ProductsMapper:
    @staticmethod
    def map_raw_data_to_product(raw_product: Dict[str, Any]) -> Product:
        """
        Maps a raw dictionary to a Product object using the Builder pattern.
        
        Args:
            raw_product: Dictionary containing product data
            
        Returns:
            Product object built and validated
            
        Raises:
            ValueError: If the data is invalid
        """
        return (Product()
            .set_id(raw_product.get('id'))
            .set_name(raw_product.get('name'))
            .set_category(raw_product.get('category'))
            .set_price(raw_product.get('price'))
            .build())