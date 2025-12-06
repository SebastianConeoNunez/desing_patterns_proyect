from pydantic import BaseModel, Field, field_validator
from typing import Optional


class UpdateUserRequestDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Updated user name")
    password: Optional[str] = Field(None, min_length=8, description="Updated password")
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        if v is None:
            return v
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v is None:
            return v
        if any(char.isdigit() for char in v):
            raise ValueError('Name cannot contain numbers')
        return v.strip()
