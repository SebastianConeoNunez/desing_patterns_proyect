import json
from typing import List, Optional
from datetime import datetime
from werkzeug.exceptions import BadRequest
from src.configurations.constants import USERS
from src.interfaces.repositories.users_repository_interface import IUsersRepository
from src.interfaces.repositories.session_interface import IDatabaseConnection
from src.models.user import User
from src.mappers.user_mapper import UserMapper


class UsersRepository(IUsersRepository):

    def __init__(self, database_connection: IDatabaseConnection):
        """
        Initializes the UsersRepository.
        
        Args:
            database_connection: Database connection instance
        """
        self.db: IDatabaseConnection = database_connection
    
    def get_all(self) -> List[User]:
        """
        Retrieves all users and maps them to User objects.
        
        Returns:
            List of mapped users, or empty list if no data exists
        """
        if self.db.data:
            raw_users = self.db.data.get(USERS, [])
            users = list(map(UserMapper.map_raw_data_to_user, raw_users))
            return users
        
        return []

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieves a single user by its ID.
        
        Args:
            user_id: The user identifier
            
        Returns:
            User object if found, None otherwise
        """
        if self.db.data:
            raw_users = self.db.data.get(USERS, [])
            for raw_user in raw_users:
                if raw_user.get('id') == user_id:
                    return UserMapper.map_raw_data_to_user(raw_user)
        
        return None

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieves a single user by email.
        
        Args:
            email: The user email
            
        Returns:
            User object if found, None otherwise
        """
        if self.db.data:
            raw_users = self.db.data.get(USERS, [])
            for raw_user in raw_users:
                if raw_user.get('email') == email.lower():
                    return UserMapper.map_raw_data_to_user(raw_user)
        
        return None

    def add_one(self, user: User) -> User:
        """
        Adds a new user to the database.
        
        Args:
            user: User object to add
            
        Returns:
            The added user with ID
            
        Raises:
            BadRequest: If email already exists
        """
        if not self.db.data:
            return None
        
        users = self.db.data.get(USERS, [])
        
        existing_emails = [u.get('email') for u in users]
        if user.email.lower() in existing_emails:
            raise BadRequest(f"Email '{user.email}' is already registered")
        
        new_id = max([u.get('id', 0) for u in users], default=0) + 1
        user.id = new_id
        
        if not user.created_at:
            user.created_at = datetime.utcnow()
        
        user_dict = UserMapper.to_dict(user)
        
        users.append(user_dict)
        self.db.data[USERS] = users
        
        with open(self.db.json_file_path, 'w') as json_file:
            json.dump(self.db.data, json_file, indent=4)
        
        return user

    def update_one(self, user: User) -> User:
        """
        Updates an existing user in the database.
        
        Args:
            user: User object with updated data
            
        Returns:
            The updated user
            
        Raises:
            BadRequest: If user not found
        """
        if not self.db.data:
            return None
        
        users = self.db.data.get(USERS, [])
        
        user_index = None
        for i, raw_user in enumerate(users):
            if raw_user.get('id') == user.id:
                user_index = i
                break
        
        if user_index is None:
            raise BadRequest(f"User with ID {user.id} not found")
        
        user.updated_at = datetime.utcnow()
        
        user_dict = UserMapper.to_dict(user)
        users[user_index] = user_dict
        
        self.db.data[USERS] = users
        
        with open(self.db.json_file_path, 'w') as json_file:
            json.dump(self.db.data, json_file, indent=4)
        
        return user

    def delete_one(self, user_id: int) -> bool:
        """
        Deletes (deactivates) a user from the database.
        Performs a soft delete by setting is_active to False.
        
        Args:
            user_id: The user identifier
            
        Returns:
            True if deletion successful, False otherwise
            
        Raises:
            BadRequest: If user not found
        """
        if not self.db.data:
            return False
        
        users = self.db.data.get(USERS, [])
        
        user_found = False
        for user_dict in users:
            if user_dict.get('id') == user_id:
                user_dict['is_active'] = False
                user_dict['updated_at'] = datetime.utcnow().isoformat()
                user_found = True
                break
        
        if not user_found:
            raise BadRequest(f"User with ID {user_id} not found")
        
        self.db.data[USERS] = users
        
        with open(self.db.json_file_path, 'w') as json_file:
            json.dump(self.db.data, json_file, indent=4)
        
        return True
