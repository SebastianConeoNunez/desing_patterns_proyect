from pydantic import BaseModel, Field, field_validator
from werkzeug.exceptions import BadRequest
import re


class RegisterRequestDTO(BaseModel):
    email: str = Field(..., description="User email (must be unique)")
    password: str = Field(..., min_length=8, description="User password (minimum 8 characters)")
    name: str = Field(..., min_length=2, max_length=100, description="User full name")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise BadRequest('Invalid email format')
        return v.lower()
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise BadRequest('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise BadRequest('Password must contain at least one digit')
        return v
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if any(char.isdigit() for char in v):
            raise BadRequest('Name cannot contain numbers')
        return v.strip()