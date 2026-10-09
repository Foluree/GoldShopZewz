from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bd_and_config.postgres_engine import get_session
from app.bd_request.apeal_added import create_appeal
from app.bd_request.hased_password.hased_cookie import get_current_profile
from app.models.appeal_model import (
    AppealAnswers,
    AppealReplyIn,
    Undertable_appeal,
)

router = APIRouter(
    prefix='/appeal_admid_check',
    tags=['appeal dialog'],
)

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / 'templates'))

_NEVER = datetime.min

def _thread_root(by_id: dict[int, Undertable_appeal], appeal_id: int) -> int | None:
    current = appeal_id
    seen: set[int] = set()

    while current not in seen:
        seen.add(current)
        appeal = by_id.get(current)
        if appeal is None:
            return None
        if not appeal.parent_id:
            return current
        current = appeal.parent_id

    return current

def _message_sort_key(message: dict):
    at = message.get('at')
    return (at if isinstance(at, datetime) else _NEVER, message['id'])

def _build_threads(appeals, answers) -> dict[int, dict]:
    by_id = {appeal.id: appeal for appeal in appeals}

    answers_by_appeal: dict[int, list] = {}
    for answer in answers:
        answers_by_appeal.setdefault(answer.appeal_id, []).append(answer)

    groups: dict[int, list] = {}
    for appeal in appeals:
        root = _thread_root(by_id, appeal.id) or appeal.id
        groups.setdefault(root, []).append(appeal)

    threads: dict[int, dict] = {}
    for root_id, group in groups.items():
        root = by_id[root_id]
        messages: list[dict] = []

        for appeal in group:
            messages.append(
                {
                    'kind': 'user',
                    'id': appeal.id,
                    'appeal_id': appeal.id,
                    'email': appeal.email_user,
                    'text': appeal.appeal,
                    'at': appeal.created_at,
                    'reaction': None,
                }
            )
            for answer in answers_by_appeal.get(appeal.id, []):
                messages.append(
                    {
                        'kind': 'moderator',
                        'id': answer.id,
                        'appeal_id': appeal.id,
                        'email': answer.email_user,
                        'text': answer.answer,
                        'at': answer.created_at,
                        'reaction': answer.reaction,
                    }
                )

        messages.sort(key=_message_sort_key)

        threads[root_id] = {
            'root_id': root_id,
            'table_name': root.table_name,
            'canceled': root.canceled,
            'messages': messages,
        }

    return threads

async def _load_user_dialogs_data(session: AsyncSession, profile_id: int):
    appeals = (
        await session.execute(
            select(Undertable_appeal)
            .where(Undertable_appeal.user_id == profile_id)
            .order_by(Undertable_appeal.id)
        )
    ).scalars().all()

    if not appeals:
        return [], {}

    answers = (
        await session.execute(
            select(AppealAnswers).where(
                AppealAnswers.appeal_id.in_([appeal.id for appeal in appeals])
            )
        )
    ).scalars().all()

    return appeals, _build_threads(appeals, answers)

def _message_payload(message: dict) -> dict:
    at = message.get('at')
    return {
        'kind': message['kind'],
        'id': message['id'],
        'appeal_id': message['appeal_id'],
        'email': message['email'],
        'text': message['text'],
        'created_at': at.isoformat() if isinstance(at, datetime) else None,
        'reaction': message.get('reaction'),
    }

async def load_user_dialogs(session: AsyncSession, profile_id: int) -> list[dict]:
    _, threads = await _load_user_dialogs_data(session, profile_id)

    dialogs = []
    for thread in threads.values():
        messages = thread['messages']
        if not messages:
            continue

        last = messages[-1]
        first_user = next(
            (message for message in messages if message['kind'] == 'user'), messages[0]
        )
        last_at = last['at'] if isinstance(last['at'], datetime) else _NEVER

        dialogs.append(
            {
                'root_id': thread['root_id'],
                'table_name': thread['table_name'],
                'canceled': thread['canceled'],
                'preview': (first_user['text'] or '')[:90],
                'last_text': last['text'] or '…',
                'last_kind': last['kind'],
                'last_at': last_at,
                'last_iso': last_at.isoformat() if last_at is not _NEVER else '',
                'awaiting_user': last['kind'] == 'moderator',
                'messages_count': len(messages),
            }
        )

    dialogs.sort(key=lambda dialog: (dialog['last_at'], dialog['root_id']), reverse=True)
    return dialogs

async def get_user_thread(session: AsyncSession, profile_id: int, appeal_id: int) -> dict | None:
    appeals, threads = await _load_user_dialogs_data(session, profile_id)
    if appeal_id not in {appeal.id for appeal in appeals}:
        return None

    by_id = {appeal.id: appeal for appeal in appeals}
    root_id = _thread_root(by_id, appeal_id) or appeal_id
    return threads.get(root_id)

@router.get('/dialog', response_class=HTMLResponse)
async def dialog_page(
    request: Request,
    appeal_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(get_session),
):
    profile = await get_current_profile(session, request)
    if not profile:
        return RedirectResponse(url='/regist/', status_code=303)

    return templates.TemplateResponse(
        'appeal_dialog.html',
        {
            'request': request,
            'appeal_id': appeal_id,
            'profile': profile,
        }
    )

@router.get('/api/dialog', status_code=200)
async def get_dialog(
    request: Request,
    appeal_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(get_session),
):
    profile = await get_current_profile(session, request)
    if not profile:
        return JSONResponse(status_code=401, content={'message': 'Required login in the auth'})

    thread = await get_user_thread(session, profile['id'], appeal_id)
    if not thread:
        return JSONResponse(status_code=404, content={'message': 'Appeal not found'})

    return {
        'root_id': thread['root_id'],
        'table_name': thread['table_name'],
        'canceled': thread['canceled'],
        'last_kind': thread['messages'][-1]['kind'],
        'messages': [_message_payload(message) for message in thread['messages']]
    }

@router.post('/api/dialog/reply', status_code=201)
async def reply_dialog(
    payload: AppealReplyIn,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    profile = await get_current_profile(session, request)
    if not profile:
        return JSONResponse(status_code=401, content={'message': 'Required login in the auth'})

    thread = await get_user_thread(session, profile['id'], payload.appeal_id)
    if not thread:
        return JSONResponse(status_code=404, content={'message': 'Appeal not found'})

    user_messages = [
        message for message in thread['messages'] if message['kind'] == 'user'
    ]
    parent_id = user_messages[-1]['id'] if user_messages else payload.appeal_id

    reply_id = await create_appeal(
        session,
        profile['id'],
        profile['email'],
        thread['table_name'],
        payload.text or '',
        parent_id=parent_id,
    )

    thread = await get_user_thread(session, profile['id'], payload.appeal_id)

    return {
        'message': 'Reply sent',
        'reply_id': reply_id,
        'root_id': thread['root_id'],
        'canceled': thread['canceled'],
        'messages': [_message_payload(message) for message in thread['messages']],
    }