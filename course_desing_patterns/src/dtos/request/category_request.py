from pydantic import BaseModel, Field

class categoryRequestDTO(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the product")
