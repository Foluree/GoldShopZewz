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

async def load_auth_user(session: AsyncSession, user_id: int) -> dict | None:
    response = await session.execute(
        text(
            "SELECT id, email_us FROM users WHERE id = :user_id"
        ),
        {"user_id": user_id}
    )

    row = response.mappings().first()
    if not row:
        return None
    return dict(row)

async def load_user_profile(session: AsyncSession, email: str) -> dict | None:
    response = await session.execute(
        text(
            'SELECT id, full_name, email, city, bonus_point '
            'FROM "UserProfiles" WHERE email = :email'
        ),
        {"email": email}
    )

    row = response.mappings().first()
    if not row:
        return None
    return dict(row)

async def create_user_profile(session: AsyncSession, email: str) -> dict:
    username = get_username_from_email(email)
    response = await session.execute(
        text(
            'INSERT INTO "UserProfiles" (full_name, email, city, bonus_point) '
            'VALUES (:full_name, :email, :city, :bonus_point) '
            'RETURNING id, full_name, email, city, bonus_point'
        ),
        {
            "full_name": username,
            "email": email,
            "city": "",
            "bonus_point": 0,
        }
    )

    await session.commit()
    return dict(response.mappings().one())

async def get_or_create_user_profile(session: AsyncSession, email: str) -> dict:
    profile = await load_user_profile(session, email)
    if profile:
        profile["bonus_point"] = profile.get("bonus_point") or 0
        profile["city"] = profile.get("city") or ""
        profile["full_name"] = profile.get("full_name") or get_username_from_email(email)
        return profile
    return await create_user_profile(session, email)

async def update_user_profile(session: AsyncSession, email: str, full_name: str, city: str) -> dict:
    response = await session.execute(
        text(
            'UPDATE "UserProfiles" '
            'SET full_name = :full_name, city = :city '
            'WHERE email = :email '
            'RETURNING id, full_name, email, city, bonus_point'
        ),
        {
            "email": email,
            "full_name": full_name.strip() or get_username_from_email(email),
            "city": city.strip(),
        }
    )

    await session.commit()
    row = response.mappings().first()
    if row:
        profile = dict(row)
    else:
        profile = await create_user_profile(session, email)
    profile["bonus_point"] = profile.get("bonus_point") or 0
    return profile

async def add_profile_purchase(
        session: AsyncSession,
        profile_id: int,
        title: str,
        quantity: int,
        total_price: float,
        status: str = "Куплено",
) -> dict: 
    response = await session.execute(
        text(
            'INSERT INTO "BayProfileItem" (title, quantity, total_price, status, bayitem_at, user_id) '
            'VALUES (:title, :quantity, :total_price, :status, CURRENT_DATE, :profile_id) '
            'RETURNING id, title, quantity, total_price, status, bayitem_at'
        ),
        {
            "title": title,
            "quantity": quantity,
            "total_price": total_price,
            "status": status,
            "profile_id": profile_id,
        }
    )
    return dict(response.mappings().one())

async def load_profile_purchases(session: AsyncSession, profile_id: int) -> list[dict]:
    response = await session.execute(
        text(
            'SELECT id, title, quantity, total_price, status, bayitem_at '
            'FROM "BayProfileItem" WHERE user_id = :profile_id ORDER BY id' 
        ),
        {"profile_id": profile_id}
    )
    return [dict(row) for row in response.mappings().all()]

async def delete_profile_purchase(session: AsyncSession, profile_id: int, purchase_id: int) -> bool:
    response = await session.execute(
        text(
        'DELETE FROM "BayProfileItem" '
        'WHERE id = :purchase_id AND user_id = :profile_id'
        ),
        {
            "purchase_id": purchase_id,
            "profile_id": profile_id,
        }
    )

    await session.commit()
    return response.rowcount > 0


def get_username_from_email(email: str) -> str:
    return email.split("@", 1)[0]