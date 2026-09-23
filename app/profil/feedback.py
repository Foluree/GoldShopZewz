from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.bd_and_config.postgres_engine import get_session
from app.bd_request.hased_password.hased_cookie import verify_accses_token
from app.bd_request.local_profile_request import load_auth_user, get_or_create_user_profile
from app.bd_request.apeal_added import create_appeal, APPEAL_TYPES
from app.models.appeal_model import (
    AppealIn,
    Undertable_appeal,
)
from sqlalchemy import select

router = APIRouter(
    prefix="/feedback",
    tags=["feedback users"]
)

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

@router.get("/", response_class=HTMLResponse) 
async def home(request: Request):
    return templates.TemplateResponse(
        "feedback.html",
        {
            "request": request,
        }
    )

@router.post("/api", status_code=201)
async def send_appeal(appeal: AppealIn, request: Request, session: AsyncSession = Depends(get_session)):
    known_types = {name for name, _ in APPEAL_TYPES}
    if appeal.table_name not in known_types:
        return JSONResponse(status_code=400, content={"message": "Unknown appeal type"})

    token = request.cookies.get("booking_accses_token")
    user_id = verify_accses_token(token)
    if not user_id:
        return JSONResponse(status_code=401, content={"message": "Required login in the auth"})

    auth_user = await load_auth_user(session, int(user_id))
    if not auth_user:
        return JSONResponse(status_code=401, content={"message": "User not found"})

    profile = await get_or_create_user_profile(session, auth_user["email_us"])

    appeal_id = await create_appeal(
        session,
        profile['id'],
        profile["email"],
        appeal.table_name,
        appeal.appeal,
    )

    return {"message": "Appeal accepted", "appeal_id": appeal_id}

@router.get("/api", status_code=200)
async def get_appeals(request: Request, session: AsyncSession = Depends(get_session)):
    token = request.cookies.get("booking_accses_token")
    user_id = verify_accses_token(token)
    if not user_id:
        return JSONResponse(status_code=401, content={"message": "Required login in the auth"})

    auth_user = await load_auth_user(session, int(user_id))
    if not auth_user:
        return JSONResponse(status_code=401, content={"message": "User not found"})

    profile = await get_or_create_user_profile(session, auth_user["email_us"])

    rows = (
        await session.execute(
            select(Undertable_appeal)
            .where(Undertable_appeal.user_id == profile["id"])
            .order_by(Undertable_appeal.id)
        )
    ).scalars().all()

    return {
        "appeals": [
            {
                "id": row.id,
                "user_id": row.user_id,
                "email_user": row.email_user,
                "table_name": row.table_name,
                "appeal": row.appeal,
            }
            for row in rows
        ]
    }

@router.get("/api/all", status_code=200)
async def get_all_appeals(session: AsyncSession = Depends(get_session)):
    rows = (
        await session.execute(
            select(Undertable_appeal).order_by(Undertable_appeal.id)
        )
    ).scalars().all()

    return {
        "appeals": [
            {
                "id": row.id,
                "user_id": row.user_id,
                "email_user": row.email_user,
                "table_name": row.table_name,
                "appeal": row.appeal,
            }
            for row in rows
        ]
    }