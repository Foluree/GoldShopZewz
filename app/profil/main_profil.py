from fastapi import APIRouter, Request, Depends, Form
#from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from app.main_title_router import templates
#from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.bd_and_config.postgres_engine import get_session
#from app.models.profile_model import UserProfiles
from app.bd_request.local_profile_request import (_load_first_exito,
                                                    response_ho,
                                                    purchase_se,
                                                    response_hos,
                                                    purchase_ses,
                                                    load_auth_user,
                                                    get_username_from_email,
                                                    update_user_profile,
                                                    load_profile_purchases,
                                                    get_or_create_user_profile,
                                                    delete_profile_purchase)
from app.bd_request.hased_password.hased_cookie import verify_accses_token

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)


async def _get_auth_user_or_redirect(requesto: Request, session: AsyncSession = Depends(get_session)):
    token = requesto.cookies.get("booking_accses_token")
    user_id = verify_accses_token(token)
    if not user_id:
        return None

    auth_user = await load_auth_user(session, int(user_id))

    return auth_user

@router.get("", response_class=HTMLResponse)
async def profile(requesto: Request, session: AsyncSession = Depends(get_session)):
    auth_user = await _get_auth_user_or_redirect(requesto, session)
    if not auth_user:
        return RedirectResponse(url="/regist/", status_code=303)

    user = await get_or_create_user_profile(session, auth_user["email_us"])
    user["purchasesAll"] = await load_profile_purchases(session, user["id"])

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": requesto,
            "profile": user,
            "saved": requesto.query_params.get('saved') == "1",
        }
    )

@router.post("", response_class=HTMLResponse)
async def update_profile(
    requesto: Request,
    full_name: str = Form(""),
    city: str = Form(""),
    session: AsyncSession = Depends(get_session),
):
    auth_user = await _get_auth_user_or_redirect(requesto, session)
    if not auth_user:
        return RedirectResponse(url="/regist/", status_code=303)

    await get_or_create_user_profile(session, auth_user["email_us"])
    await update_user_profile(session, auth_user["email_us"], full_name, city)

    return RedirectResponse(url="/profile?saved=1", status_code=303)

@router.delete("/purchases/{purchase_id}")
async def cancel_purchase(
    purchase_id: int,
    requesto: Request,
    session: AsyncSession = Depends(get_session),
):
    auth_user = await _get_auth_user_or_redirect(requesto, session)
    if not auth_user:
        return JSONResponse({"detail": "not authenticated"}, status_code=401)

    user = await get_or_create_user_profile(session, auth_user["email_us"])
    deleted = await delete_profile_purchase(session, user["id"], purchase_id)
    if not deleted:
        return JSONResponse({"detail": "purchase not found"}, status_code=404)

    return JSONResponse({"deleted": True})