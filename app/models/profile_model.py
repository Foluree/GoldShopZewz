from pydantic import BaseModel, EmailStr
from datetime import date

class BayProfileItem(BaseModel):
    id: int
    title: str
    quantity: int
    total_price: float
    status: str
    bayitem_at: date

class UserProfiles(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    city: str
    bonus_point: int
    purchasesAll: list[BayProfileItem]