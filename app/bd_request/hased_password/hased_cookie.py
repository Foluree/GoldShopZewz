from app.bd_and_config.config1 import setbase
from passlib.context import CryptContext

cmd_txt = CryptContext(schemes="bcrypt", deprecated="auto")

def get_cookie_password(code: str) -> str:
    return cmd_txt.hash(code)

