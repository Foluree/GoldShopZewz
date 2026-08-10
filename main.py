from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.main_title_router import router as router_main_lob
from app.profil.main_profil import router as router_profile
from app.profil.logins_user import router as router_login
from app.profil.register_user import router as router_regist
from app.profil.setting_user import router as router_sett
from app.bd_request.send_startup import seed_all_on_startup


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_all_on_startup()
    yield

app = FastAPI(title="Gold Shop", lifespan=lifespan)

app.include_router(router_sett)
app.include_router(router_profile)                         
app.include_router(router_main_lob)                                          
app.include_router(router_login)
app.include_router(router_regist)