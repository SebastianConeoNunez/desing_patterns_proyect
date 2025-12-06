import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound
from src.utils.common import Common
from src.interfaces.services.auth_service_interface import IAuthService
from src.interfaces.repositories.users_repository_interface import IUsersRepository
from src.dtos.request.register_request import RegisterRequestDTO
from src.dtos.request.login_request import LoginRequestDTO
from src.models.user import User
from src.mappers.user_mapper import UserMapper


class AuthService(IAuthService):
    
    def __init__(self, users_repository: IUsersRepository ):
        self.db = users_repository
        self.secret_key = os.getenv("JWT_SECRET_KEY")
        self.token_expiration_hours = int(os.getenv("JWT_EXPIRATION_HOURS"))
    
    def register(self, register_dto: RegisterRequestDTO) -> dict:
        """
        Register a new user in the system.
        
        Args:
            register_dto: DTO with registration data (email, password, name)
            
        Returns:
            dict: User data without password (JSON serializable)
        """
        if not register_dto:
            raise BadRequest("Registration data is required")
        
        existing_user = self.db.get_by_email(register_dto.email)
        if existing_user:
            raise BadRequest(f"Email '{register_dto.email}' is already registered")
        
        hashed_password = Common.hash_password(register_dto.password)
        
        user: User = UserMapper.from_register_dto(register_dto, hashed_password)
        
        created_user = self.db.add_one(user)
        
        return UserMapper.to_response(created_user)
    
    def login(self, login_dto: LoginRequestDTO) -> dict:
        """
        Authenticate user and generate JWT token.
        
        Args:
            login_dto: DTO with login credentials (email, password)
            
        Returns:
            dict: Token and user data (JSON serializable)
        """
        if not login_dto:
            raise BadRequest("Login credentials are required")
        
        user = self.db.get_by_email(login_dto.email)
        if not user:
            raise Unauthorized("Invalid email or password")
        
        if not self._verify_password(login_dto.password, user.password):
            raise Unauthorized("Invalid email or password")
        
        if not user.is_active:
            raise Unauthorized("User account is deactivated")
        
        token = self._generate_token(user)
        
        return {
            "token": token,
            "user": UserMapper.to_response(user)
        }
    
    def validate_token(self, token: str) -> dict:
        """
        Validate JWT token and return user data.
        
        Args:
            token: JWT token string
            
        Returns:
            dict: User data if token is valid
        """
        if not token:
            raise BadRequest("Token is required")
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            user_id = payload.get('user_id')
            
            if not user_id:
                raise Unauthorized("Invalid token payload")
            
            user = self.db.get_by_id(user_id)
            if not user:
                raise Unauthorized("User not found")
            
            if not user.is_active:
                raise Unauthorized("User account is deactivated")
            
            return UserMapper.to_response(user)
            
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Token has expired")
        except jwt.InvalidTokenError:
            raise Unauthorized("Invalid token")
    
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hashed password."""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def _generate_token(self, user: User) -> str:
        """Generate JWT token for user."""
        payload = {
            'user_id': user.id,
            'email': user.email,
            'role': user.role.value,
            'exp': datetime.utcnow() + timedelta(hours=self.token_expiration_hours),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token
