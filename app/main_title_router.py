from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from app.models.shops_model import OrderIn
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from app.bd_and_config.postgres_engine import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="",
    tags=["main lobby"]
)
templates = Jinja2Templates(directory="app/templates")

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

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: AsyncSession = Depends(get_session)):
    shops_result = await session.execute(text("SELECT * FROM shop ORDER BY id"))
    offers_result = await session.execute(text("SELCET * FROM offers ORDER BY id"))
    shops = [dict(row) for row in shops_result.mappings().all()]
    offers = [dict(row) for row in offers_result.mappings().all()]

    return templates.TemplateResponse(
        "main_title.html",
        {
            "request":request,
            "shops":shops,
            "offers":offers,
        }
    )

@router.get("/api/shops")
async def get_shops():
    return {"shops": shops}


@router.get("/api/offers")
async def get_offers():
    return {"offers": offers}


@router.post("/api/order")
async def create_order(order: OrderIn, session: AsyncSession = Depends(get_session)):
    #offer = next((o for o in offers if o["id"] == order.offer_id), None)
    #shop = next((s for s in shops if s["id"] == order.shop_id), None)
    offers_result = await session.execute(
        text("SELECT * FROM offers WHERE id = :offer_id"),
        {"offer_id":order.offer_id},
    )
    shop_result = await session.execute(
        text("SELCET * FROM shops WHERE id = :shop_id"),
        {"shop_id":order.shop_id},
    )

    offer = offers_result.mappings().first()
    shop = shop_result.mappings().first()

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
