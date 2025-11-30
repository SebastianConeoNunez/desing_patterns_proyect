from typing import List
from src.interfaces.repositories.products_repository_interface import IProductsRepository
from src.interfaces.repositories.session_interface import IDatabaseConnection
from src.models.product import Product
from src.mappers.products_mapper import ProductsMapper


class ProductsRepository(IProductsRepository):

    def __init__(self, database_connection: IDatabaseConnection):
        """
        Initializes the ProductsRepository.
        
        Args:
            database_connection: Database connection instance
        """
        self.db: IDatabaseConnection = database_connection
    
    def get_all(self, category_filter: str = None) -> List[Product]:
        """
        Retrieves all products and maps them to Product objects.
        
        Args:
            category_filter: Optional category to filter products
        
        Returns:
            List of mapped products, or empty list if no data exists
        """
        if self.db.data:
            raw_products = self.db.data.get('products', [])
            products = list(map(ProductsMapper.map_raw_data_to_product, raw_products))
            
            if category_filter:
                return [p for p in products if p.category == category_filter]
            
            return products
        
        return []

    def get_one_by_id(self, product_id: int) -> Product:
        """
        Retrieves a single product by its ID.
        
        Args:
            product_id: The product identifier
            
        Returns:
            Product object if found, None otherwise
        """
        if self.db.data:
            raw_products = self.db.data.get('products', [])
            for raw_product in raw_products:
                if raw_product.get('id') == product_id:
                    return ProductsMapper.map_raw_data_to_product(raw_product)
        
        return None

    def add_one(self, product: Product) -> Product:
        """
        Adds a new product to the database.
        
        Args:
            product: Product object to add
            
        Returns:
            The added product with ID
        """
        if self.db.data:
            products = self.db.data.get('products', [])
            
            new_id = max([p.get('id', 0) for p in products], default=0) + 1
            product.id = new_id
            
            product_dict = {
                'id': product.id,
                'name': product.name,
                'category': product.category,
                'price': product.price
            }
            
            products.append(product_dict)
            self.db.data['products'] = products            
            return product
        
        return None