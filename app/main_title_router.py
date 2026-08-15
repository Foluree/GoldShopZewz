from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from app.models.shops_model import OrderIn, ShopCreate, OfferCreate
from app.models.shops1_model import Shops
from app.models.offers_model import Offers  
from fastapi.templating import Jinja2Templates
from sqlalchemy import text, insert
from app.bd_and_config.postgres_engine import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.bd_request.nortal_request import _fetch_all, _fetch_one
from re import search

router = APIRouter(
    prefix="",
    tags=["main lobby"]
)
templates = Jinja2Templates(directory="app/templates")

_WEIGHT_BY_GAMES = {"1":"1g", "5":"5g", "10":"10g"}

def _offer_weight(title: str) -> str:
    match1 = search(r"(\d+)", title or "")
    return _WEIGHT_BY_GAMES.get(match1.group(1), "") if match1 else ""

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: AsyncSession = Depends(get_session)):

    shops = await _fetch_all(session, "shops")
    offers = await _fetch_all(session, "offers")

    for offer in offers:
        offer["weight"] = _offer_weight(offer.get("title", ""))

    return templates.TemplateResponse(
        "main_title.html",
        {
            "request":request,
            "shops":shops,
            "offers":offers,
        }
    )

@router.post("/api/shops", status_code=201)
async def create_shop(shop: ShopCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        insert(Shops)
        .values(**shop.model_dump())
        .returning(Shops.id, Shops.name, Shops.address, Shops.hours, Shops.phone,
                   Shops.quantity_1g, Shops.quantity_5g, Shops.quantity_10g)
    )
    await session.commit()
    create_shop = result.mappings().one()
    return {"shop": dict(create_shop)}


@router.post("/api/offers", status_code=201)
async def create_offer(offer: OfferCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        insert(Offers)
        .values(**offer.model_dump())
        .returning(Offers.id, Offers.title, Offers.price, Offers.price)
    )
    await session.commit()
    create_offer = result.mappings().one()
    return {"Offers": dict(create_offer)}


@router.get("/api/shops")
async def get_shops(session: AsyncSession = Depends(get_session)):
    shops = await _fetch_all(session, "shops")
    return {"shops": shops}


@router.get("/api/offers")
async def get_offers(session: AsyncSession = Depends(get_session)):
    offers = await _fetch_all(session, "offers")
    return {"offers": offers}


@router.post("/api/order", status_code=201)
async def create_order(order: OrderIn, session: AsyncSession = Depends(get_session)):
    shop = await _fetch_one(session, "shops", order.shop_id)
    offer = await _fetch_one(session, "offers", order.offer_id)

    if not offer:
        return JSONResponse(status_code=404, content={"message": "Товар не найден"})
    if not shop:
        return JSONResponse(status_code=404, content={"message": "Магазин не найден"})

    order_result = await session.execute(
        text(
            'INSERT INTO "OrderIn" (offer_id, shop_id, quantity) '
            'VALUES (:offer_id, :shop_id, :quantity) '
            'RETURNING id, offer_id, shop_id, quantity '
        ),
        order.model_dump(),
    )

    await session.commit()
    created_order = dict(order_result.mappings().one())

    total = offer["price"] * order.quantity
    return {
        "message": (
            f"Заказ принят: {order.quantity} × {offer['title']} "
            f"в точке '{shop['name']}'. Сумма: {total:.2f} €"
        ),
        "order": created_order
    }


