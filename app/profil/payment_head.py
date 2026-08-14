from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse

router = APIRouter(
    prefix="/payment",
    tags=["Payment user"]
)

@router.get("/", response_class=HTMLResponse)
async def payment_page():
    return FileResponse("app/templates/payment_1.html")
