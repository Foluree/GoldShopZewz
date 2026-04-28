from fastapi import APIRouter, Request, Depends
#from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse#, JSONResponse
from app.main_title_router import templates
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.bd_and_config.postgres_engine import get_session
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
async def profile(requesto: Request, session: AsyncSession = Depends(get_session)):
    user_result = await session.execute(text("SELECT * FROM users WHERE id = 1"))
    purchases_result = await session.execute(
        text("SELECT id, title, quantity, total_price, status, bayitem_at "
             "FROM purchases WHERE user_id = 1 ORDER BY id")
    )
    
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": requesto,
            "profile": profile_data
        }
    )

#@router.get("/api")
