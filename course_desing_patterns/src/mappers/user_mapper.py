from typing import Dict, Any
from datetime import datetime
from src.models.user import User
from src.enums.user_role import UserRole
from src.dtos.request.register_request import RegisterRequestDTO


class UserMapper:
    
    @staticmethod
    def map_raw_data_to_user(raw_data: Dict[str, Any]) -> User:
        """
        Maps a raw dictionary to a User object using the Builder pattern.
        
        Args:
            raw_data: Dictionary containing user data from database
            
        Returns:
            User object built and validated
        """
        user = (User()
            .set_id(raw_data.get('id'))
            .set_email(raw_data['email'])
            .set_password(raw_data['password'])
            .set_name(raw_data['name'])
            .set_role(UserRole(raw_data.get('role', 'customer')))
            .set_is_active(raw_data.get('is_active', True)))
        
        if raw_data.get('created_at'):
            if isinstance(raw_data['created_at'], str):
                user.set_created_at(datetime.fromisoformat(raw_data['created_at']))
            else:
                user.set_created_at(raw_data['created_at'])
        
        if raw_data.get('updated_at'):
            if isinstance(raw_data['updated_at'], str):
                user.set_updated_at(datetime.fromisoformat(raw_data['updated_at']))
            else:
                user.set_updated_at(raw_data['updated_at'])
        
        return user.build()
    
    @staticmethod
    def to_dict(user: User) -> Dict[str, Any]:
        """
        Converts a User model to a dictionary for JSON storage.
        
        Args:
            user: User object
            
        Returns:
            Dictionary with all user fields including password
        """
        return {
            'id': user.id,
            'email': user.email,
            'password': user.password,
            'name': user.name,
            'role': user.role.value,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None,
            'is_active': user.is_active
        }
   
    @staticmethod
    def to_response(user: User) -> Dict[str, Any]:
        """
        Converts a User model to a response dictionary (without password).
        
        Args:
            user: User object
            
        Returns:
            Dictionary without sensitive fields like password
        """
        return {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role.value,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'is_active': user.is_active
        }
    
    @staticmethod
    def from_register_dto(dto: RegisterRequestDTO, hashed_password: str) -> User:
        """
        Converts a RegisterRequestDTO to a User model.
        
        Args:
            dto: Registration DTO
            hashed_password: Already hashed password
            
        Returns:
            User object ready to be saved
        """
        return (User()
            .set_email(dto.email)
            .set_password(hashed_password)
            .set_name(dto.name)
            .set_role(UserRole.CUSTOMER)
            .set_created_at(datetime.utcnow())
            .build())
    
