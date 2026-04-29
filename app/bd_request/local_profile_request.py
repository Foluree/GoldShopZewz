from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

response_ho = "SELECT id, full_name, email, city, bonus_point FROM users WHERE id = 1" 
response_hos ='SELECT id, full_name, email, city, bonus_point FROM "UserProfiles" WHERE id = 1'

purchase_ses = 'SELECT id, title, quantity, total_price, status, bayitem_at FROM "BayProfileItem" WHERE user_id = 1 ORDER BY id'
purchase_se = 'SELECT id, title, quantity, total_price, status, bayitem_at FROM "BayProfileItem ORDER BY id"' #BayProfileItem

async def _load_first_exito(session: AsyncSession, queries: list[str]) -> list[dict]:
    for query in queries:
        try:
            response = await session.execute(text(query))
            return [dict(rows) for rows in response.mappings().all()]
        except Exception as e:
            print(e)
            continue
    return []