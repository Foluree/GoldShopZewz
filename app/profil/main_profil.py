from fastapi import APIRouter, Request, Depends
#from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse#, JSONResponse
from app.main_title_router import templates
#from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.bd_and_config.postgres_engine import get_session
#from app.models.profile_model import UserProfiles
from app.bd_request.local_profile_request import _load_first_exito, response_ho, purchase_se, response_hos, purchase_ses
from app.bd_request.hased_password.hased_cookie import verify_accses_token

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)


@router.get("", response_class=HTMLResponse)
async def profile(requesto: Request, session: AsyncSession = Depends(get_session)):
    token = requesto.cookies.get("booking_accses_token")
    user_id = verify_accses_token(token)
    if not user_id:
        return RedirectResponse(url="/regist/", status_code=303)
    
    users = await _load_first_exito(session, [
                                        response_hos,
                                        response_hos,],
                                    )

    purchases = await _load_first_exito(session,
                                        [purchase_ses,
                                         purchase_ses,],
                                        )

    user = users[0] if users else {
        "full_name":"Пользователь",
        "email":"-",
        "city":"-",
        "bonus_point":0
    }

    user["purchasesAll"] = purchases

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": requesto,
            "profile": user
        }
    )

#@router.get("/api")
