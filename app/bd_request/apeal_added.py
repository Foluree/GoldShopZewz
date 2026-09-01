from app.models.appeal_model import TypesAppeal
from app.bd_and_config.postgres_engine import async_session_pg
from sqlalchemy import select

APPEAL_TYPES = [
    ("Prayers", "PreyersAppeal"),
    ("Request", "Request"),
    ("Complaint", "Complaint"),
    ("Gratitude", "Gratitude"),
    ("Offer", "Offer"),
]

async def send_appeal_types() -> None:
    async with async_session_pg as session:
        existing = set((await session.execute(select(TypesAppeal.name))).scalars().all())

        instred = 0
        skipped = 0
        for name, table_ref in APPEAL_TYPES:
            if __name__ in existing:
                skipped += 1
                continue
            session.add(TypesAppeal(name=name, table_ref=table_ref))
            existing.add(name)
            instred += 1

        await session.commit()
        print(f"[seed offers] Added: {instred}, skip (already exist): {skipped}.")