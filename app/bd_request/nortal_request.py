from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert
from app.bd_and_config.postgres_engine import async_session_pg

async def _fetch_all(session: AsyncSession, table_variants: str) -> list[dict]:
    return await session.execute(text(f"SELECT * FROM {table_variants} ORDER BY id"))

async def _fetch_one(session: AsyncSession, vatinats: str, record_id: int) -> list | None:
    response = await session.execute(
        text(f"SELECT * FROM {vatinats} WHERE id = :record_id"),
        {"record_id":record_id}
        )
    rows = response.mappings().first()
    return dict(rows) if rows else None

class BaseSeo:

    modeli = None

    @classmethod
    async def find_one_finger(cls, **filmer_by):
        async with async_session_pg() as session:
            namber=select(cls.modeli).filter_by(**filmer_by)
            question = await session.execute(namber)
            return question.scalar_one_or_none()

    @classmethod
    async def finger_allin(cls, **date_base):
        async with async_session_pg() as session:
            namber = insert(cls.modeli).values(**date_base)
            await session.execute(namber)
            await session.commit()