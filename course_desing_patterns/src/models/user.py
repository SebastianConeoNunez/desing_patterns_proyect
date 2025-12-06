import re
from datetime import datetime
from src.enums.user_role import UserRole


class User:
    def __init__(self):
        self.id = None
        self.email = None
        self.password = None
        self.name = None
        self.role = None
        self.created_at = None
        self.updated_at = None
        self.is_active = True

    def set_id(self, id: int):
        self.id = id
        return self
    
    def set_email(self, email: str):
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        self.email = email.lower()
        return self

    def set_password(self, password: str):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        self.password = password
        return self

    def set_name(self, name: str):
        if not name or len(name.strip()) == 0:
            raise ValueError("Name cannot be empty")
        self.name = name.strip()
        return self

    def set_role(self, role: UserRole):
        if not isinstance(role, UserRole):
            raise ValueError("Invalid role")
        self.role = role
        return self
    
    def set_created_at(self, created_at: datetime):
        self.created_at = created_at
        return self
    
    def set_updated_at(self, updated_at: datetime):
        self.updated_at = updated_at
        return self
    
    def set_is_active(self, is_active: bool):
        self.is_active = is_active
        return self
    
    def build(self):
        if not self.email:
            raise ValueError("User must have an email")
        if not self.password:
            raise ValueError("User must have a password")
        if not self.name:
            raise ValueError("User must have a name")
        if not self.role:
            self.role = UserRole.CUSTOMER 
        if not self.created_at:
            self.created_at = datetime.utcnow()
        return self
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format using regex."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def __repr__(self):
        return f"<User id={self.id}, email={self.email}, name={self.name}, role={self.role}>"
