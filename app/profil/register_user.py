from fastapi import APIRouter#, Depends, Response
from app.models.model_register import Registro
from app.models.model_user.users_seo import UsersSeo
from app.bd_request.hased_password.hased_cookie import get_cookie_password
from app.bd_and_config.error_bs.main_error import UserAllNoneExit

router = APIRouter(
    prefix="/regist",
    tags=["Registor User"]
)

@router.post("/")
async def regist_use(user_data: Registro):
    mb_new_user = await UsersSeo.find_one_finger(email_us=user_data.email_us)
    if mb_new_user:
        raise UserAllNoneExit
    refresho = get_cookie_password(user_data.passuse)
    await UsersSeo.finger_allin(email_us=user_data.email_us, hases_password_us=refresho)
