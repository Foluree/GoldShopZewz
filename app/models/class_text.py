from pydantic import Field, BaseModel

class OrderIn(BaseModel):
    offer_id: int = Field(..., gt=0)
    shop_id: int = Field(..., gt=0)
    quantity: int = Field(1, gt=0)

class BuyIn(BaseModel):
    weight: str = Field(..., min_length=1, max_length=5)

class OfferCreate(BaseModel):
    title: str = Field(..., min_length=1)
    price: float =  Field(..., gt=0)
    desc: str = Field(..., min_length=1)

class ShopCreate(BaseModel):
    name: str = Field(..., min_length=1)
    address: str = Field(..., min_length=1)
    hours: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)
    quantity_1g: int = Field(..., ge=0)
    quantity_5g: int = Field(..., ge=0)
    quantity_10g: int = Field(..., ge=0)