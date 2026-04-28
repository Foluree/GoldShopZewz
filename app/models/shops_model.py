#from pydantic import Field
from app.bd_and_config.postgres_engine import Base_Pg
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer

class OrderIn(Base_Pg):
    __tablename__ = "OrderIn"

    id: Mapped[int] = mapped_column(primary_key=True)

    offer_id: Mapped[int] = mapped_column(Integer)
    shop_id: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer, default=1)