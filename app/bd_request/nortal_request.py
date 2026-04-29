from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

async def _fetch_all(session: AsyncSession, table_variants: str) -> list[dict]:
    return await session.execute(text(f"SELECT * FROM {table_variants} ORDER BY id"))

async def _fetch_one(session: AsyncSession, vatinats: str, record_id: int) -> list | None:
    response = await session.execute(
        text(f"SELECT * FROM {vatinats} WHERE id = :record_id"),
        {"record_id":record_id}
        )
    rows = response.mappings().first()
    return dict(rows) if rows else None