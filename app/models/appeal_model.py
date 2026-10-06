from pydantic import BaseModel, Field
from app.bd_and_config.postgres_engine import Base_Pg
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Date, ForeignKey, Boolean, text
from app.models.profile_model import UserProfiles


class Undertable_appeal(Base_Pg):
    __tablename__ = "Undertable_appeal"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("UserProfiles.id")) 
    email_user: Mapped[str] = mapped_column(String)

    table_name: Mapped[str] = mapped_column(String)
    appeal: Mapped[str] = mapped_column(String)

    canceled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("false"))

class PreyersAppeal(Undertable_appeal):
    __tablename__ = "PrayersAppeal"

    id: Mapped[int] = mapped_column(ForeignKey("Undertable_appeal.id"), primary_key=True)

class Request(Undertable_appeal):
    __tablename__ = "Request"

    id: Mapped[int] = mapped_column(ForeignKey("Undertable_appeal.id"), primary_key=True)

class Complaint(Undertable_appeal):
    __tablename__ = "Complaint"

    id: Mapped[int] = mapped_column(ForeignKey("Undertable_appeal.id"), primary_key=True)

class Gratitude(Undertable_appeal):
    __tablename__ = "Gratitude"

    id: Mapped[int] = mapped_column(ForeignKey("Undertable_appeal.id"), primary_key=True)


class TypesAppeal(Base_Pg):
    __tablename__ = "TypesAppeal"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String)
    table_ref: Mapped[str] = mapped_column(String)


class AppealAnswers(Base_Pg):
    __tablename__ = "AppealAnswers"

    id: Mapped[int] = mapped_column(primary_key=True)

    appeal_id: Mapped[int] = mapped_column(ForeignKey("Undertable_appeal.id"))
    reaction: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("UserProfiles.id"))
    email_user: Mapped[str] = mapped_column(String)

    answer: Mapped[str] = mapped_column(String, default="")


class AppealIn(BaseModel):
    table_name: str = Field(..., min_length=1)
    appeal: str = Field(..., min_length=1)

class AppealModerationIn(BaseModel):
    appeal_id: int = Field(..., ge=1)
    reaction: bool = False
    answer: str = ""