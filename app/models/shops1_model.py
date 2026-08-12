from app.bd_and_config.postgres_engine import Base_Pg
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
#from datetime import date

class Shops(Base_Pg):
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    hours: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    quantity_1g: Mapped[int] = mapped_column(Integer, default=0)
    quantity_5g: Mapped[int] = mapped_column(Integer, default=0)
    quantity_10g: Mapped[int] = mapped_column(Integer, default=0)