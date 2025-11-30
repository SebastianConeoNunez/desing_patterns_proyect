from flask import Flask
from flask_restful import Api
from src.controllers.categories_controller import categories_bp, set_categories_service
from src.services.categories_service import CategoriesService
from src.repositories.category_repository import CategoriesRepository
from src.repositories.session import DatabaseConnection
from src.controllers.products_controller import products_bp, set_products_service
from src.services.products_service import ProductsService
from src.repositories.product_repository import ProductsRepository

app = Flask(__name__)
api = Api(app)

def configure_dependencies():
    """Initialize and inject dependencies."""
    db_connection = DatabaseConnection('db.json')
    db_connection.connect()
    
    products_repository = ProductsRepository(db_connection)
    category_repository = CategoriesRepository(db_connection)
    
    products_service = ProductsService(products_repository)
    category_service = CategoriesService(category_repository)
    
    set_products_service(products_service)
    set_categories_service(category_service)

configure_dependencies()

app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(categories_bp, url_prefix='/categories')

# import json
# with open('db.json', 'r') as file:
#     products = json.load(file)

# api.add_resource( AuthenticationResource,'/auth')

# api.add_resource(FavoritesResource, '/favorites')

if __name__ == '__main__':
    app.run(debug=True)

