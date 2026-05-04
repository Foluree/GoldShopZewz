from fastapi import APIRouter, Request, Form, HTTPException#, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse 
from fastapi.templating import Jinja2Templates
from app.models.model_register import Registro
from app.models.model_user.users_seo import UsersSeo
from app.bd_request.hased_password.hased_cookie import get_cookie_password
from app.bd_and_config.error_bs.main_error import UserAllNoneExit

router = APIRouter(
    prefix="/regist",
    tags=["Registor User"]
)

templating = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def regist_html(request: Request):
    return templating.TemplateResponse(
        "split_register.html",{
            "request":request,
        }
    )

#@router.post("/api")
async def _create_user(user_data: Registro):
    mb_new_user = await UsersSeo.find_one_finger(email_us=user_data.email_us)
    if mb_new_user:
        raise UserAllNoneExit
    refresho = get_cookie_password(user_data.passuse)
    await UsersSeo.finger_allin(email_us=user_data.email_us, hases_password_us=refresho)

@router.post("/api")
async def register_use_api(user_data: Registro):
    await _create_user(user_data)
    return {"status":"ok"}

@router.post("/log", response_class=HTMLResponse)
async def regist_use_form(
    request: Request,
    email_us: str = Form(...),
    passuse: str = Form(...),
    passuse_confirm: str = Form(...),
):
    if passuse != passuse_confirm:
        return templating.TemplateResponse(
            "split_register.html",
            {"request": request, "error_message": "Password no confirm."},
            status_code=400
        )
    
    try:
        await _create_user(Registro(email_us=email_us,passuse=passuse))

    except HTTPException as e:
        if e.status_code == 409:
            return templating.TemplateResponse(
                "split_register.html",
                {"request" : request, "error_message" : "Error Password or Email."},
                status_code=400
            )
        
        raise e
    
    return RedirectResponse(url="/login/", status_code=303)

 