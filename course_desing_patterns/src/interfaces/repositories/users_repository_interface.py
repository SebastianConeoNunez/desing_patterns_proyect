from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.user import User


class IUsersRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[User]:
        """Retrieve all users from the database."""
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a single user by ID."""
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a single user by email."""
    
    @abstractmethod
    def add_one(self, user: User) -> User:
        """Add a new user to the database."""
    
    @abstractmethod
    def update_one(self, user: User) -> User:
        """Update an existing user in the database."""
    
    @abstractmethod
    def delete_one(self, user_id: int) -> bool:
        """Delete (deactivate) a user from the database."""
