from pydantic import BaseModel, Field


class FavoriteRequestDTO(BaseModel):
    user_id: int = Field(..., description="id of the user")
    product_id: int = Field(..., description="id of the product")
