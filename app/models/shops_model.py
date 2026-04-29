from pydantic import Field, BaseModel

class OrderIn(BaseModel):
    offer_id: int = Field(..., gt=0)
    shop_id: int = Field(..., gt=0)
    quantity: int = Field(1, gt=0)