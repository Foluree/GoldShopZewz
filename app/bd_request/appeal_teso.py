from app.models.appeal_model import (
    Undertable_appeal,
    PreyersAppeal,
    Request,
    Complaint,
    Gratitude,
    TypesAppeal,
)
from app.bd_and_config.postgres_engine import async_session_pg
from app.bd_request.local_profile_request import get_or_create_user_profile
from sqlalchemy import select

APPEAL_TYPES = [
    ("Prayers", "PreyersAppeal"),
    ("Request", "Request"),
    ("Complaint", "Complaint"),
    ("Gratitude", "Gratitude"),
    ("Offer", "Offer"),
]

APPEAL_SUBCLASSES = {
    "Prayers": PreyersAppeal,
    "Request": Request,
    "Complaint": Complaint,
    "Gratitude": Gratitude,
}

DEMO_APPEALS = [
    (
        "Prayers",
        "Пусть Зевс хранит моё новое золото и приносит удачу в делах, "
        "чтобы слитки только росли в цене и не терялись.",
    ),
    (
        "Request",
        "Прошу зарезервировать слиток 5 г в магазине на Елисейских полях "
        "и уведомить, когда его можно будет забрать лично.",
    ),
    (
        "Complaint",
        "Слиток 1 г пришёл с царапиной на блистере. Прошу проверить качество "
        "упаковки перед отгрузкой, чтобы избежать повреждений при доставке.",
    ),
    (
        "Gratitude",
        "Спасибо за быструю доставку и полный комплект сертификатов "
        "подлинности. Всем доволен, закажу ещё раз.",
    ),
    (
        "Offer",
        "Предлагаю оптовое сотрудничество по скупке лома золота. "
        "Готов обсудить объёмы поставок и цены на золото.",
    ),
]

async def send_appeal_types() -> None:
    async with async_session_pg() as session:
        existing = set((await session.execute(select(TypesAppeal.name))).scalars().all())

        inserted = 0
        skipped = 0
        for name, table_ref in APPEAL_TYPES:
            if name in existing:
                skipped += 1
                continue
            session.add(TypesAppeal(name=name, table_ref=table_ref))
            existing.add(name)
            inserted += 1

        await session.commit()
        print(f"[seed appeal types] Added: {inserted}, skip (already exist): {skipped}.")

async def create_appeal(session, user_id: int, email_user: str, table_name: str, appeal: str) -> int:
    base = Undertable_appeal(
        user_id=user_id,
        email_user=email_user,
        table_name=table_name,
        appeal=appeal,
    )
    session.add(base)
    await session.flush()

    subclass = APPEAL_SUBCLASSES.get(table_name)
    if subclass:
        session.add(subclass(id=base.id))

    await session.commit()
    return base.id

async def seed_appeals() -> None:
    async with async_session_pg() as session:
        existing = set((await session.execute(select(Undertable_appeal.appeal))).scalars().all())

        profile = await get_or_create_user_profile(session, "demo@gold.olympus")

        inserted = 0
        skipped = 0
        for table_name, appeal in DEMO_APPEALS:
            if appeal in existing:
                skipped += 1
                continue
            await create_appeal(session, profile["id"], profile["email"], table_name, appeal)
            existing.add(appeal)
            inserted += 1

        print(f"[seed appeals] Added: {inserted}, skip (already exist): {skipped}.")