from abc import ABC, abstractmethod
from src.dtos.request.register_request import RegisterRequestDTO
from src.dtos.request.login_request import LoginRequestDTO


class IAuthService(ABC):

    @abstractmethod
    def register(self, register_dto: RegisterRequestDTO) -> dict:
        """Register a new user in the system."""

    @abstractmethod
    def login(self, login_dto: LoginRequestDTO) -> dict:
        """Authenticate user and generate JWT token."""

