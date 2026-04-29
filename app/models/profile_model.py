#from pydantic import EmailStr
from datetime import date
from app.bd_and_config.postgres_engine import Base_Pg
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Date, ForeignKey

class BayProfileItem(Base_Pg):
    __tablename__ = "BayProfileItem"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    quantity: Mapped[int] = mapped_column(Integer)
    total_price: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String)
    bayitem_at: Mapped[date] = mapped_column(Date)

    user_id: Mapped[int] = mapped_column(ForeignKey("UserProfiles.id"))
    user: Mapped["UserProfiles"] = relationship("UserProfiles", back_populates="purchasesAll")

class UserProfiles(Base_Pg):
    __tablename__ = "UserProfiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    bonus_point: Mapped[int] = mapped_column(Integer)
    purchasesAll: Mapped[list[BayProfileItem]] = relationship("BayProfileItem",
                                                              back_populates="user")