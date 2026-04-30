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
