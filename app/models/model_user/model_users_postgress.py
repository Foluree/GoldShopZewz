from sqlalchemy import Column, Integer, String
from app.bd_and_config.postgres_engine import Base_Pg
from sqlalchemy.orm import Mapped, mapped_column

class users(Base_Pg):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email_us: Mapped[str] = mapped_column(String)
    hases_password_us: Mapped[str] = mapped_column(String)
