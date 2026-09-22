from app.models.appeal_model import (
    Undertable_appeal,
    PreyersAppeal,
    Request,
    Complaint,
    Gratitude,
    TypesAppeal,
)
from app.bd_and_config.postgres_engine import async_session_pg
from sqlalchemy import select
from app.bd_request.local_profile_request import get_or_create_user_profile

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
        "Пусть Зевс хранит мое новое золото и приносит удачу в делах, "
        "чтобы слитки только росли в цене и не терялись.",
    ),
    (
        "Request",
        "Прошу зарезевировать слиток 5 г в мазазине на Елисейских полях "
        "и уведомить, когда его будет можно забрать мне лично.",
    ),
    (
        "Complaint",
        "Слиток 1 г пришел с царапиной на блистере. Прошу проверить качество "
        "упаковки перед отгрузкой, чтобы избежать повреждений при доставке.",
    ),
    (
        "Gratitude",
        "Спасибо за быструю доставку и полный коплект сертификатов "
        "подлиности. Всем доволен, закажу еще раз."
    ),
    (
        "Offer",
        "Предлогаю оптовое сотрудничество по скупке лома золота. "
        "Готов обсудить обьемы поставок и цены на золото.",
    ),
]

async def send_appeal_types() -> None:
    async with async_session_pg() as session:
        existing = set((await session.execute(select(TypesAppeal.name))).scalars().all())

        instred = 0
        skipped = 0
        for name, table_ref in APPEAL_TYPES:
            if name in existing:
                skipped += 1
                continue
            session.add(TypesAppeal(name=name, table_ref=table_ref))
            existing.add(name)
            instred += 1

        await session.commit()
        print(f"[seed offers] Added: {instred}, skip (already exist): {skipped}.")

async def create_appeal(session, user_id: int, email_user: str, table_name: str, appeal: str) -> int:
    subclass = APPEAL_SUBCLASSES.get(table_name)
    if subclass:
        appeal_obj = subclass(
            user_id=user_id,
            email_user=email_user,
            table_name=table_name,
            appeal=appeal,
        )
    else:
        appeal_obj = Undertable_appeal(
            user_id=user_id,
            email_user=email_user,
            table_name=table_name,
            appeal=appeal,
        )

    session.add(appeal_obj)

    await session.commit()

    return appeal_obj.id


async def seed_appeals() -> None:
    async with async_session_pg() as session:
        existing = set((await session.execute(select(Undertable_appeal.appeal))).scalars().all())

        profile = await get_or_create_user_profile(session, "demo@gold.olumpus")

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