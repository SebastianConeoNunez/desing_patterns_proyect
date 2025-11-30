from werkzeug.exceptions import BadRequest, NotFound
from src.dtos.request.create_product_request import ProductCreateDTO
from src.interfaces.repositories.products_repository_interface import IProductsRepository
from src.interfaces.services.products_service_interface import IProductsService
from src.mappers.products_mapper import ProductsMapper
from src.models.product import Product

class ProductsService(IProductsService):
    def __init__(self, products_repository: IProductsRepository):
        self.db = products_repository
    
    def get_all(self, category_filter:str=None)->list:
        """
        Method to get all products.

        Args:
            category_filter (str, optional): Category to filter products. Defaults to None.

        Returns:
            List of products as dictionaries (JSON serializable)
        """
        products:list[Product] = self.db.get_all(category_filter)
        
        if category_filter and not products:
            raise NotFound(f"No products found for category '{category_filter}'")
        
        return [
            {
                "id": product.id,
                "name": product.name,
                "category": product.category,
                "price": product.price
            }
            for product in products
        ]
    
    def get_one_by_id(self, product_id:int)->dict:
        """
        Method to get one product by id

        Args:
            product_id (int): product identifier

        Returns:
            dict: product data as dictionary (JSON serializable)
        """
        if not product_id:
            raise BadRequest("Product ID is required")
        
        product = self.db.get_one_by_id(product_id)
        if not product:
            raise NotFound(f"Product with ID {product_id} not found")
        
        return {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "price": product.price
        }

    def create_one(self, product_data: ProductCreateDTO)->dict:
        """ 
        Method to create one product.

        Args:
            product_data (ProductCreateDTO): data to create product
        
        Returns:
            dict: created product as dictionary (JSON serializable)
        """
        if not product_data:
            raise BadRequest("Product data is required")
        
        product:Product = ProductsMapper.map_raw_data_to_product(product_data.model_dump())
        
        created_product = self.db.add_one(product)
        
        return {
            "id": created_product.id,
            "name": created_product.name,
            "category": created_product.category,
            "price": created_product.price
        }
       
        


