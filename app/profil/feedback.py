from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi.templating import Jinja2Templates

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
