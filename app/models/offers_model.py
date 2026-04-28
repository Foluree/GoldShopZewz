from app.bd_and_config.postgres_engine import Base_Pg
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float

class Offers(Base_Pg):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    desc: Mapped[str] = mapped_column(String)