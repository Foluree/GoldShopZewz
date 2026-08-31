from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.bd_and_config.postgres_engine import get_session
from app.bd_request.hased_password.hased_cookie import _get_auth_user_or_redirect
from pathlib import Path
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent.parent / "templates"

router = APIRouter(
    prefix="/payment",
    tags=["Payment user"]
)

templates = Jinja2Templates(directory=str(BASE_DIR))


@router.get("/", response_class=HTMLResponse)
async def payment_page(request: Request, session: AsyncSession = Depends(get_session)):
    auth_user = await _get_auth_user_or_redirect(request, session)
    if not auth_user:
        return RedirectResponse(url="/regist/", status_code=303)

    return templates.TemplateResponse("payment_1.html", {"request": request})