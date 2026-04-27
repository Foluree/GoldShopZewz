from fastapi import FastAPI#, Request
#from fastapi.responses import HTMLResponse, JSONResponse
#from pydantic import BaseModel
from app.main_title_router import router as router_main_lob
from app.profil.main_profil import router as router_profile

app = FastAPI(title="Gold Shop")

app.include_router(router_profile)
app.include_router(router_main_lob) 