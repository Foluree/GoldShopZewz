from fastapi import APIRouter, Request, Depends
#from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse#, JSONResponse
from app.main_title_router import templates
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.bd_and_config.postgres_engine import get_session
from app.models.profile_model import UserProfiles
from app.bd_request.local_profile_request import _load_first_exito, response_ho, purchase_se, response_hos, purchase_ses

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)

"""
profile_data = UserProfiles(
    id=1,
    full_name="Дима Пригожин", 
    email="test@gmail.com",
    city="Вильнес",
    bonus_point=240,
    purchasesAll=[
        {
            "id":1,
            "title":"Золото 1 г",
            "quantity":1,
            "total_price":92.5,
            "status":"Выдано",
            "bayitem_at":"2026-04-20"
        },
        {
            "id":2,
            "title":"Золото 5 г",
            "quantity":2,
            "total_price":910.0,
            "status":"Готов к выдаче",
            "bayitem_at":"2026-04-26"
        }
    ]
)
"""

@router.get("", response_class=HTMLResponse)
async def profile(requesto: Request, session: AsyncSession = Depends(get_session)):
    users = await _load_first_exito(session, [
                                        response_hos,
                                        response_hos,],
                                    )

    purchases = await _load_first_exito(session,
                                        [purchase_ses,
                                         purchase_ses,],
                                        )
    
    print(users)

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
