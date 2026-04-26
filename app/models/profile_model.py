from pydantic import BaseModel, EmailStr
from datetime import data

class BayProfileItem(BaseModel):
    id: int
    title: str
    quantity: int
    total_price: float
    status: str
    bayitem_at: data

class UserProfiles(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    city: str
    bonus_point: int
    purchasesAll: list[BayProfileItem]