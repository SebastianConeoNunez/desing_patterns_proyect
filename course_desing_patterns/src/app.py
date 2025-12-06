from flask import Flask
from flask_restful import Api
from src.services.auth_service import AuthService
from src.controllers.auth_controller import  auth_bp,set_auth_service
from src.controllers.users_controller import users_bp,set_users_service
from src.services.users_service import UsersService
from src.repositories.users_repository import UsersRepository
from src.controllers.favorites_controller import favorites_bp, set_favorites_service
from src.services.favorites_service import FavoritesService
from src.repositories.favorites_repository import FavoritesRepository
from src.configurations.constants import CATEGORIES, FAVORITES, PRODUCTS
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
    favorites_repository = FavoritesRepository(db_connection)
    user_repository = UsersRepository(db_connection)
    
    products_service = ProductsService(products_repository)
    category_service = CategoriesService(category_repository)
    favorites_service = FavoritesService(favorites_repository)
    user_service = UsersService(user_repository)
    auth_service = AuthService(user_repository)
    
    set_products_service(products_service)
    set_categories_service(category_service)
    set_favorites_service(favorites_service)
    set_users_service(user_service)
    set_auth_service(auth_service)

configure_dependencies()

app.register_blueprint(products_bp, url_prefix=f'/{PRODUCTS}')
app.register_blueprint(categories_bp, url_prefix=f'/{CATEGORIES}')
app.register_blueprint(favorites_bp, url_prefix=f'/{FAVORITES}')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(users_bp, url_prefix='/users')


if __name__ == '__main__':
    app.run(debug=True)

