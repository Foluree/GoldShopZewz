import os
import sys

from sqlalchemy import select

from app.bd_and_config.postgres_engine import async_session_pg
from app.models.offers_model import Offers
from app.models.shops1_model import Shops

_EXTERNAL_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "External_Added"
)

if _EXTERNAL_DIR not in sys.path:
    sys.path.insert(0, _EXTERNAL_DIR)

from load_gold_price_1 import PRICES
from load_shops_1 import SHOPS

async def seed_offers() -> None:
    async with async_session_pg() as session:
        existing = set((await session.execute(select(Offers.title))).scalars().all())

        inserted = 0
        skipped = 0
        for title, price, desc in PRICES:
            if title in existing:
                skipped += 1
                continue
            session.add(Offers(title=title, price=price, desc=desc))
            existing.add(title)
            inserted += 1

        await session.commit()
        print(f"[seed offers] Added: {inserted}, skip (already exist): {skipped}.")

async def seed_shops() -> None:
    async with async_session_pg() as session:
        existing = set((await session.execute(select(Shops.name))).scalars().all())

        inserted = 0
        skipped = 0
        for name, address, hours, phone, qty_1g, qty_5g, qty_10g in SHOPS:
            if name in existing:
                skipped += 1
                continue
            session.add(Shops(name=name, address=address, hours=hours, phone=phone, quantity_1g=qty_1g, quantity_5g=qty_5g, quantity_10g=qty_10g))
            existing.add(name)
            inserted += 1

        await session.commit()
        print(f"[seed shops] Added: {inserted}, skip (already exist): {skipped}")

async def seed_all_on_startup() -> None:
    try:
        await seed_offers()
    except Exception as exc:
        print(f"[seed offers] failed on startup: {exc}")

    try:
        await seed_shops()
    except Exception as exc:
        print(f"[seed shops] failed on startup: {exc}")