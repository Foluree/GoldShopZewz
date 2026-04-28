from app.bd_and_config.postgres_engine import Base_Pg
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
#from datetime import date

class Shops(Base_Pg):
    __tablename__ = "Shops"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    hours: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)