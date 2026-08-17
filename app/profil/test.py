from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.bd_and_config.postgres_engine import get_session
from app.bd_request.local_profile_request import load_auth_user
from app.bd_request.hased_password.hased_cookie import verify_accses_token

router = APIRouter(
    prefix="/payment",
    tags=["Payment user"]
)

@router.get("/", response_class=HTMLResponse)
async def payment_page(request: Request, session: AsyncSession = Depends(get_session)):
    token = request.cookies.get("booking_accses_token")
    user_id = verify_accses_token(token)
    if not user_id:
        return RedirectResponse(url="/regist/", status_code=303)

    auth_user = await load_auth_user(session, int(user_id))
    if not auth_user:
        return RedirectResponse(url="/regist/", status_code=303)

    return FileResponse("app/templates/payment_1.html")
