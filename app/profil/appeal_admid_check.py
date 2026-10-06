from pathlib import Path

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bd_and_config.postgres_engine import get_session
from app.bd_request.hased_password.hased_cookie import verify_accses_token
from app.bd_request.local_profile_request import load_auth_user, get_or_create_user_profile
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

async def _moderator_profile(session: AsyncSession, request: Request) -> dict:
    try:
        token = request.cookies.get('booking_accses_token')
        user_id = verify_accses_token(token)
        if user_id:
            auth_user = await load_auth_user(session, int(user_id))
            if auth_user:
                return await get_or_create_user_profile(session, auth_user['email_us'])
    except Exception as exc:
        print(f'[appeal moderate] auth profile failed, fallback used: {exc}')

    return await get_or_create_user_profile(session, _MODERATOR_FALLBACK_EMAIL)


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
async def get_answers(session: AsyncSession = Depends(get_session)):
    rows = (
        await session.execute(select(AppealAnswers).order_by(AppealAnswers.id))
    ).scalars().all()

    return {
        "answers": [
            {
                "id": row.id,
                "appeal_id": row.appeal_id,
                "reaction": row.reaction,
                "user_id": row.user_id,
                "email_user": row.email_user,
                "answer": row.answer,
            }
            for row in rows
        ]
    }