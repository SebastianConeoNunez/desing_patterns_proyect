from pydantic import BaseModel, Field, EmailStr


class LoginRequestDTO(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")

