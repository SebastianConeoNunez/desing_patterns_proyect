from flask import Flask
from flask_restful import Api
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
    
    products_service = ProductsService(products_repository)
    
    set_products_service(products_service)

configure_dependencies()

app.register_blueprint(products_bp, url_prefix='/products')

# import json
# with open('db.json', 'r') as file:
#     products = json.load(file)

# api.add_resource( AuthenticationResource,'/auth')

# api.add_resource(CategoriesResource, '/categories', '/categories/<int:category_id>')

# api.add_resource(FavoritesResource, '/favorites')

if __name__ == '__main__':
    app.run(debug=True)

