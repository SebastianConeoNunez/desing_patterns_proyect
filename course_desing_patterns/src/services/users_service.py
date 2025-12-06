from werkzeug.exceptions import BadRequest, NotFound
from src.utils.common import Common
from src.interfaces.services.users_service_interface import IUsersService
from src.interfaces.repositories.users_repository_interface import IUsersRepository
from src.dtos.request.update_user_request import UpdateUserRequestDTO
from src.models.user import User
from src.mappers.user_mapper import UserMapper


class UsersService(IUsersService):
    
    def __init__(self, users_repository: IUsersRepository):
        self.db = users_repository
    
    def get_all(self) -> list:
        """
        Get all users from the system.
        
        Returns:
            list: List of users as dictionaries (JSON serializable)
        """
        users: list[User] = self.db.get_all()
        
        return [
            UserMapper.to_response(user)
            for user in users
        ]
    
    def get_by_id(self, user_id: int) -> dict:
        """
        Get a user by ID.
        
        Args:
            user_id: User identifier
            
        Returns:
            dict: User data as dictionary (JSON serializable)
        """
        if not user_id:
            raise BadRequest("User ID is required")
        
        user = self.db.get_by_id(user_id)
        if not user:
            raise NotFound(f"User with ID {user_id} not found")
        
        return UserMapper.to_response(user)
    
    def update_one(self, user_id: int, update_dto: UpdateUserRequestDTO) -> dict:
        """
        Update user information.
        
        Args:
            user_id: User identifier
            update_dto: DTO with fields to update
            
        Returns:
            dict: Updated user data (JSON serializable)
        """
        if not user_id:
            raise BadRequest("User ID is required")
        
        if not update_dto:
            raise BadRequest("Update data is required")
        
        user = self.db.get_by_id(user_id)
        if not user:
            raise NotFound(f"User with ID {user_id} not found")
        
        if update_dto.name is not None:
            user.set_name(update_dto.name)
        
        if update_dto.password is not None:
            hashed_password = Common.hash_password(update_dto.password)
            user.set_password(hashed_password)
        
        user.build()
        updated_user = self.db.update_one(user)
        
        return UserMapper.to_response(updated_user)
    
    def delete_one(self, user_id: int) -> bool:
        """
        Delete (deactivate) a user account.
        
        Args:
            user_id: User identifier
            
        Returns:
            bool: True if deletion successful
        """
        if not user_id:
            raise BadRequest("User ID is required")
        
        user = self.db.get_by_id(user_id)
        if not user:
            raise NotFound(f"User with ID {user_id} not found")
        
        deleted = self.db.delete_one(user_id)
        
        if not deleted:
            raise BadRequest("Failed to delete user")
        
        return True
    
    
