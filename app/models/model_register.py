from pydantic import BaseModel, EmailStr

class Registro(BaseModel):
    email_us: EmailStr
    passuse: str