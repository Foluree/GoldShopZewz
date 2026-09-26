from pathlib import Path

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bd_and_config.postgres_engine import get_session
from app.models.appeal_model import Undertable_appeal, TypesAppeal

router = APIRouter(
    prefix="/appeal_admid_check",
    tags=["appeal admin check"],
)

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

_DEFAULT_TYPES = ["Prayers", "Request", "Complaint", "Gratitude", "Offer"]


async def _category_names(session: AsyncSession) -> list[str]:
    rows = (
        await session.execute(select(TypesAppeal.name).order_by(TypesAppeal.id))
    ).scalars().all()
    return list(rows) or _DEFAULT_TYPES 


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: AsyncSession = Depends(get_session)):
    categories = await _category_names(session)

    rows = (
        await session.execute(select(Undertable_appeal).order_by(Undertable_appeal.id))
    ).scalars().all()

    appeals = [
        {
            "id": row.id,
            "user_id": row.user_id,
            "email_user": row.email_user,
            "table_name": row.table_name,
            "appeal": row.appeal,
        }
        for row in rows
    ]

    return templates.TemplateResponse(
        "appeal_admid_check.html",
        {
            "request": request,
            "categories": categories,
            "appeals": appeals,
        }
    )