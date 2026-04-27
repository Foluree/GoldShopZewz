from fastapi import APIRouter, Request
#from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse#, JSONResponse
from app.main_title_router import templates
from app.models.profile_model import UserProfiles

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)

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


@router.get("", response_class=HTMLResponse)
async def profile(requesto: Request):
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": requesto,
            "profile": profile_data
        }
    )