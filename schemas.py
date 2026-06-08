from pydantic import BaseModel, ConfigDict, Field, StringConstraints, StrictInt,field_validator
from typing import Optional
from typing_extensions import Annotated
class CartBase(BaseModel):
    coupon: Optional[str] = Field(
            default=None, 
            min_length=3, 
            max_length=20, 
            pattern=r"^[A-Za-z0-9]+$",
            
        )
    @field_validator('coupon', mode='before')
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v
class CartCreate(CartBase):
    user_id: StrictInt = Field(..., le=2147483647, ge=1) 
class CartResponse(CartBase):
    id: int
    user_id: int
    status: str
    model_config = ConfigDict(from_attributes=True)
class CartItemBase(BaseModel):
    product_id: StrictInt = Field(..., le=2147483647, ge=1)
    quantity: StrictInt = Field(default=1, le=1000, ge=1)
class CartItemCreate(CartItemBase):
    pass 
class CartItemResponse(CartItemBase):
    id: int
    cart_id: int
    price_at_addition: float
    model_config = ConfigDict(from_attributes=True)