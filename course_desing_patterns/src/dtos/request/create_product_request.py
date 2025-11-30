from pydantic import BaseModel, Field

class ProductCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the product")
    category: str = Field(..., min_length=1, description="Category of the product")
    price: float = Field(..., gt=0, description="Price of the product")
