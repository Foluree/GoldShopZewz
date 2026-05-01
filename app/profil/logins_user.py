from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.model_register import Registro
from app.bd_and_config.error_bs.main_error import NoneCorrectEmailOrPassword
from app.bd_request.hased_password.hased_cookie import autotification_user, create_newst_token

router = APIRouter(
    prefix="/login",
    tags=["login user"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "split_login.html",
        {
            "request":request,
        }
    )

@router.post("/log")
async def logins_cookie(result: Response, user_datas: Registro):
    login = await autotification_user(user_datas.email_us, user_datas.passuse)
    if not login:
        raise NoneCorrectEmailOrPassword
    accses_new_tok = create_newst_token({"sub":str(login.id)})
    result.set_cookie("booking_accses_token", accses_new_tok, httponly=True)
    return {"accses_token": accses_new_tok}