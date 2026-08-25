from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.main_title_router import router as router_main_lob
from app.profil.main_profil import router as router_profile
from app.profil.logins_user import router as router_login
from app.profil.register_user import router as router_regist
from app.profil.setting_user import router as router_sett
from app.profil.payment_head import router as router_payment
from app.bd_request.send_startup import seed_all_on_startup
from app.profil.api_routers_response_tempotaly import router as router_api_temporaly


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_all_on_startup()
    yield

    
app = FastAPI(title="Gold Shop", lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).resolve().parent / "app" / "tamplates_css")),
    name="static",
)

app.include_router(router_api_temporaly)
app.include_router(router_payment)
app.include_router(router_sett)
app.include_router(router_profile)                         
app.include_router(router_main_lob)                                          
app.include_router(router_login)
app.include_router(router_regist)