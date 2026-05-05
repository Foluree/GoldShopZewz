from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/settings",
    tags=["settings user"]
)

templating = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def settings_user(request: Request):
    return templating.TemplateResponse(
        "settings.html",{ 
            "request":request
        }
    )
