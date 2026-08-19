from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.bd_and_config.postgres_engine import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.bd_request.nortal_request import _fetch_all
from re import search

router = APIRouter( 
    prefix="",
    tags=["main lobby"]
)
templates = Jinja2Templates(directory="app/templates")

_WEIGHT_BY_GAMES = {"1":"1g", "5":"5g", "10":"10g"}


def _offer_weight(title: str) -> str:
    match1 = search(r"(\d+)", title or "")
    return _WEIGHT_BY_GAMES.get(match1.group(1), "") if match1 else ""

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: AsyncSession = Depends(get_session)):

    shops = await _fetch_all(session, "shops")
    offers = await _fetch_all(session, "offers")

    for offer in offers:
        offer["weight"] = _offer_weight(offer.get("title", ""))

    return templates.TemplateResponse(
        "main_title.html",
        {
            "request":request,
            "shops":shops,
            "offers":offers,
        }
    )