from pathlib import Path

from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bd_and_config.postgres_engine import get_session
from app.bd_request.hased_password.hased_cookie import get_current_profile
from app.bd_request.local_profile_request import get_or_create_user_profile
from app.models.appeal_model import (
    AppealAnswers,
    AppealModerationIn,
    Undertable_appeal,
    TypesAppeal,
)

router = APIRouter(
    prefix="/appeal_admid_check",
    tags=["appeal admin check"],
)

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

_DEFAULT_TYPES = ["Prayers", "Request", "Complaint", "Gratitude", "Offer"]
_MODERATOR_FALLBACK_EMAIL = 'moderator@gold.olumpus'


async def _category_names(session: AsyncSession) -> list[str]:
    rows = (
        await session.execute(select(TypesAppeal.name).order_by(TypesAppeal.id))
    ).scalars().all()
    return list(rows) or _DEFAULT_TYPES 

async def _moderator_profile(session: AsyncSession, request: Request) -> dict:
    profile = await get_current_profile(session, request)
    if profile:
        return profile

    return await get_or_create_user_profile(session, _MODERATOR_FALLBACK_EMAIL)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: AsyncSession = Depends(get_session)):
    categories = await _category_names(session)

    rows = (
        await session.execute(select(Undertable_appeal).order_by(Undertable_appeal.id))
    ).scalars().all()

    answer_rows = (
        await session.execute(select(AppealAnswers).order_by(AppealAnswers.id))
    ).scalars().all()

    last_answers: dict[int, AppealAnswers] = {}
    for answer_row in answer_rows:
        last_answers[answer_row.appeal_id] = answer_row

    appeals = []
    for row in rows:
        last_answer = last_answers.get(row.id)
        appeals.append(
            {
                "id": row.id,
                "user_id": row.user_id,
                'email_user': row.email_user,
                'table_name': row.table_name,
                'appeal': row.appeal,
                'canceled': row.canceled,
                'parent_id': row.parent_id,
                'answered': last_answer is not None,
                'reaction': last_answer.reaction if last_answer else None,
                'answer': (last_answer.answer if last_answer else '') or '',
                'answer_email': last_answer.email_user if last_answer else '',
            }
        )

    return templates.TemplateResponse(
        "appeal_admid_check.html",
        {
            "request": request,
            "categories": categories,
            "appeals": appeals,
        }
    )

@router.post('/api/moderate', status_code=201)
async def moderate_appeal(
    payload: AppealModerationIn,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    appeal = await session.get(Undertable_appeal, payload.appeal_id)
    if not appeal:
        return JSONResponse(status_code=404, content={"message": "Appeal not found"})

    moderator = await _moderator_profile(session, request)

    appeal.canceled = not payload.reaction

    answer = AppealAnswers(
        appeal_id=appeal.id,
        reaction=payload.reaction,
        user_id=moderator['id'],
        email_user=moderator["email"],
        answer=(payload.answer or "").strip(),
    )
    session.add(answer)

    await session.commit()

    return {
        "message": "Appeal accepted" if payload.reaction else "Appeal rejected",
        'appeal_id': appeal.id,
        'canceled': appeal.canceled,
        'reaction': answer.reaction,
        'answer_id': answer.id,
        'answer': answer.answer,
        'moderator_id': answer.user_id,
        'moderator_email': answer.email_user,
    }

@router.get('/api/answers', status_code=200)
async def get_answers(
    appeal_id: int | None = Query(None, ge=1, description='Filer by one appeal id'),
    session: AsyncSession = Depends(get_session),
):
    stmt = (
        select(AppealAnswers, Undertable_appeal)
        .outerjoin(Undertable_appeal, AppealAnswers.appeal_id == Undertable_appeal.id)
        .order_by(AppealAnswers.id)
    )
    if appeal_id:
        stmt = stmt.where(AppealAnswers.appeal_id == appeal_id)

    rows = (await session.execute(stmt)).all()

    return {
        "total": len(rows),
        "answers": [
            {
                'id': answer.id,
                'appeal_id': answer.appeal_id,
                'reaction': answer.reaction,
                'user_id': answer.user_id,
                'email_user': answer.email_user,
                'answer': answer.answer,
                'created_at': answer.created_at.isoformat() if answer.created_at else None,
                'appeal': {
                    'table_name': appeal.table_name if appeal else None,
                    'email_user': appeal.email_user if appeal else None,
                    'text': appeal.appeal if appeal else None,
                    'canceled': appeal.canceled if appeal else None,    
                },
            }
            for answer, appeal in rows
        ],
    }

