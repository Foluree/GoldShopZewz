from app.bd_and_config.config1 import setbase
from passlib.context import CryptContext
from pydantic import EmailStr
from app.models.model_user.users_seo import UsersSeo
from datetime import timedelta, datetime
from jose import jwt

cmd_txt = CryptContext(schemes="bcrypt", deprecated="auto")

def get_cookie_password(code: str) -> str:
    return cmd_txt.hash(code)

def verify_cookie(areplain, hashed_newst) -> bool:
    return cmd_txt.verify(areplain, hashed_newst)

def create_newst_token(count: dict) -> str:
    prest_code = count.copy()
    last_time = datetime.utcnow() + timedelta(minutes=30)
    prest_code.update({"exp":last_time})
    new_code = jwt.encode(
        prest_code, setbase.HASED, setbase.HASED_CODING,
    )
    return new_code

async def autotification_user(email_us: EmailStr, passuse: str):
    login = await UsersSeo.find_one_finger(email_us=email_us)
    if not login and not verify_cookie(passuse, login.hases_password_us):
        return None
    return login