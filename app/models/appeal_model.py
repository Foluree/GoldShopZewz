from app.bd_and_config.postgres_engine import Base_Pg
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Date, ForeignKey


class Undertable_appeal(Base_Pg):
    __tablename__ = "Undertable_appeal"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("UserProfiles.id"))
    email_user: Mapped[str] = mapped_column(String)

    table_name: Mapped[str] = mapped_column(String)
    appeal: Mapped[str] = mapped_column(String)

class PreyersAppeal(Undertable_appeal):
    __tablename__ = "PrayersAppeal"

class Request(Undertable_appeal):
    __tablename__ = "Request"

class Complaint(Undertable_appeal):
    __tablename__ = "Complaint"

class Gratitude(Undertable_appeal):
    __tablename__ = "Gratitude"


class TypesAppeal(Base_Pg):
    __tablename__ = "TypesAppeal"

    id: Mapped[int] = mapped_column(primary_key=True)

    name = Mapped[str] = mapped_column(String)
    table_ref = Mapped[str] = mapped_column(String)