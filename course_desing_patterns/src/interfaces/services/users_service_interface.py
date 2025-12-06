from abc import ABC, abstractmethod
from src.dtos.request.update_user_request import UpdateUserRequestDTO


class IUsersService(ABC):

    @abstractmethod
    def get_all(self) -> list:
        """Retrieve all users."""

    @abstractmethod
    def get_by_id(self, user_id: int) -> dict:
        """Retrieve a user by ID."""

    @abstractmethod
    def update_one(self, user_id: int, update_dto: UpdateUserRequestDTO) -> dict:
        """Update user information."""

    @abstractmethod
    def delete_one(self, user_id: int) -> bool:
        """Delete (deactivate) a user account."""
