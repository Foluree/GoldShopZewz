from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from app.models.shops_model import OrderIn
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from app.bd_and_config.postgres_engine import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.bd_request.nortal_request import _fetch_all, _fetch_one

router = APIRouter(
    prefix="",
    tags=["main lobby"]
)
templates = Jinja2Templates(directory="app/templates")

"""
shops = [
    {
        "id": 1,
        "name": "Центральный магазин",
        "address": "г. Вильнюс, ул. Пилес, 10",
        "hours": "09:00–20:00",
        "phone": "+370 600 00001",
    },
    {
        "id": 2,
        "name": "Магазин на проспекте",
        "address": "г. Вильнюс, пр-т Гедимина, 25",
        "hours": "10:00–21:00",
        "phone": "+370 600 00002",
    },
    {
        "id": 3,
        "name": "Торговая точка у парка",
        "address": "г. Каунас, ул. Лайсвес, 77",
        "hours": "10:00–19:00",
        "phone": "+370 600 00003",
    },
]

offers = [
    {
        "id": 101,
        "title": "Золото 1 г",
        "price": 92.5,
        "desc": "Подходит для первого заказа и подарков.",
    },
    {
        "id": 102,
        "title": "Золото 5 г",
        "price": 455.0,
        "desc": "Популярный вариант для инвестиций.",
    },
    {
        "id": 103,
        "title": "Золото 10 г",
        "price": 899.0,
        "desc": "Выгодная покупка по лучшей цене за грамм.",
    },
]
"""



@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: AsyncSession = Depends(get_session)):

    shops = await _fetch_all(session, "shops")
    offers = await _fetch_all(session, "offers")

    return templates.TemplateResponse(
        "main_title.html",
        {
            "request":request,
            "shops":shops,
            "offers":offers,
        }
    )

@router.get("/api/shops")
async def get_shops(session: AsyncSession = Depends(get_session)):
    shops = await _fetch_all(session, "shops")
    return {"shops": shops}


@router.get("/api/offers")
async def get_offers(session: AsyncSession = Depends(get_session)):
    offers = await _fetch_all(session, "offers")
    return {"offers": offers}


@router.post("/api/order")
async def create_order(order: OrderIn, session: AsyncSession = Depends(get_session)):
    shop = await _fetch_one(session, "shops", order.shop_id)
    offer = await _fetch_one(session, "offers", order.offer_id)

    if not offer:
        return JSONResponse(status_code=404, content={"message": "Товар не найден"})
    if not shop:
        return JSONResponse(status_code=404, content={"message": "Магазин не найден"})

    total = offer["price"] * order.quantity
    return {
        "message": (
            f"Заказ принят: {order.quantity} × {offer['title']} "
            f"в точке '{shop['name']}'. Сумма: {total:.2f} €"
        )
    }
