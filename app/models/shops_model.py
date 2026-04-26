from pydantic import BaseModel

class OrderIn(BaseModel):
    offer_id: int
    shop_id: int
    quantity: int = 1