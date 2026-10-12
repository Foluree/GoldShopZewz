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

    all_appeals = (
        await session.execute(
            select(Undertable_appeal).order_by(Undertable_appeal.id)
        )
    ).scalars().all()

    all_answers = (
        await session.execute(
            select(AppealAnswers).order_by(AppealAnswers.id)
        )
    ).scalars().all()

    parent_of = {a.id: a.parent_id for a in all_appeals}

    def root_of(appeal_id: int) -> int:
        seen = set()
        cur = appeal_id
        while cur is not None and cur not in seen:
            seen.add(cur)
            p = parent_of.get(cur)
            if p is None:
                return cur
            cur = p
        return cur

    groups: dict[int, list] = {}
    for a in all_appeals:
        groups.setdefault(root_of(a.id), []).append(a)

    answers_by_appeal: dict[int, list] = {}
    for ans in all_answers:
        answers_by_appeal.setdefault(ans.appeal_id, []).append(ans)

    appeals = []
    reply_total: dict[int, int] = {}

    for root_id, group in groups.items():
        group_sorted = sorted(group, key=lambda x: x.id)
        last_user = group_sorted[-1]
        reply_total[root_id] = len(group_sorted) - 1

        last_mod = None
        for a in group_sorted:
            for ans in answers_by_appeal.get(a.id, []):
                if last_mod is None or ans.id > last_mod.id:
                    last_mod = ans

        appeals.append({
            'id': last_user.id,
            "root_id": root_id,
            'user_id': last_user.user_id,
            'email_user': last_user.email_user,
            'table_name': last_user.table_name,
            'appeal': last_user.appeal,
            'canceled': last_user.canceled,
            'parent_id': None if last_user.id == root_id else root_id,
            'answered': last_mod is not None,
            'reaction': last_mod.reaction if last_mod else None,
            'answer': (last_mod.answer if last_mod else "") or "",
            'answer_email': last_mod.email_user if last_mod else "",
        })

    appeals.sort(key=lambda x: x["id"], reverse=True)

    return templates.TemplateResponse(
        'appeal_admid_check.html', 
        {
            'request': request, 
            'categories': categories,
            'appeals': appeals,
            'reply_total': reply_total,
        },
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