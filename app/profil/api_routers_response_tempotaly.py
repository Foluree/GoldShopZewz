from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from app.models.shops_model import OrderIn, ShopCreate, OfferCreate, BuyIn
from app.models.shops1_model import Shops
from app.models.offers_model import Offers  
from sqlalchemy import text, insert
from app.bd_and_config.postgres_engine import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.bd_request.nortal_request import _fetch_all, _fetch_one
from app.bd_request.hased_password.hased_cookie import verify_accses_token
from app.bd_request.local_profile_request import (
    load_auth_user,
    get_or_create_user_profile,
    add_profile_purchase,
)
from app.main_title_router import _offer_weight

router = APIRouter(
    prefix="/api",
    tags=["accses admins"]
)

_WEIGHT_COLUMNS = {
    "1g": "quantity_1g",
    "5g": "quantity_5g",
    "10g": "quantity_10g",
}

_FALLBACK_PRICES = {"1g": 130.00, "5g": 650.00, "10g": 1300.00}

def _price_for_weight(offers: list[dict], weight: str) -> float:
    for offer in offers:
        if _offer_weight(offer.get("title", "")) == weight:
            return float(offer.get("price") or 0)
    return _FALLBACK_PRICES.get(weight, 0.0)

@router.post("/shops", status_code=201)
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


@router.post("/offers", status_code=201)
async def create_offer(offer: OfferCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        insert(Offers)
        .values(**offer.model_dump())
        .returning(Offers.id, Offers.title, Offers.price, Offers.price)
    )
    await session.commit()
    create_offer = result.mappings().one()
    return {"Offers": dict(create_offer)}


@router.get("/shops")
async def get_shops(session: AsyncSession = Depends(get_session)):
    shops = await _fetch_all(session, "shops")
    return {"shops": shops}


@router.post("/shops/{shop_id}/buy")
async def buy_from_shop(shop_id: int, buy: BuyIn, request: Request, session: AsyncSession = Depends(get_session)):
    token = request.cookies.get("booking_accses_token")
    user_id = verify_accses_token(token)
    if not user_id:
        return JSONResponse(status_code=401, content={"message": "Required login in the auth"})

    auth_user = await load_auth_user(session, int(user_id))
    if not auth_user:
        return JSONResponse(status_code=401, content={"message": "User not found"})

    profile = await get_or_create_user_profile(session, auth_user["email_us"])

    column = _WEIGHT_COLUMNS.get(buy.weight)
    if not column:
        return JSONResponse(status_code=400, content={"message": "Неверный вес"})

    shop = await _fetch_one(session, "shops", shop_id)
    if not shop:
        return JSONResponse(status_code=404, content={"message": "Магазин не найден"})

    if shop.get(column, 0) <= 0:
        return JSONResponse(status_code=400, content={"message": "Товара нет в наличии"})

    offers = await _fetch_all(session, "offers")
    price = _price_for_weight(offers, buy.weight)

    result = await session.execute(
        text(
            f'UPDATE shops SET {column} = {column} - 1 '
            'WHERE id = :shop_id '
            'RETURNING quantity_1g, quantity_5g, quantity_10g'
        ),
        {"shop_id": shop_id},
    )
    quantities = dict(result.mappings().one())

    purchase = await add_profile_purchase(
        session,
        profile["id"],
        title=f"Gold ingot {buy.weight} - {shop['name']}",
        quantity=1,
        total_price=price,
    )
    await session.commit()

    return {
        "shop_id": shop_id,
        "weight": buy.weight,
        "quantities": quantities,
        "purchase": purchase,
        }


@router.get("/offers")
async def get_offers(session: AsyncSession = Depends(get_session)):
    offers = await _fetch_all(session, "offers")
    return {"offers": offers}


@router.post("/order", status_code=201)
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