from pydantic import BaseModel, ConfigDict
from typing import Optional

# 1. This MUST come first so the other classes can inherit from it
class CartBase(BaseModel):
    coupon: Optional[str] = None

# 2. Now Python knows what CartBase is when it reads this line
class CartCreate(CartBase):
    user_id: int 


class CartResponse(CartBase):
    id: int
    user_id: int
    status: str

    model_config = ConfigDict(from_attributes=True)

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1
    price_at_addition: float

class CartItemCreate(CartItemBase):
    pass 

class CartItemResponse(CartItemBase):
    id: int
    cart_id: int

    model_config = ConfigDict(from_attributes=True)