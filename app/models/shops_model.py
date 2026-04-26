from pydantic import BaseModel, Field

class OrderIn(BaseModel):
    offer_id: int
    shop_id: int
    quantity: int = Field(default=1, ge=1)