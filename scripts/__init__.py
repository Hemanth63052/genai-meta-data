from fastapi import APIRouter
from scripts.services.user import user_router
from scripts.services.login_router import login_router

all_routers = APIRouter()

all_routers.include_router(login_router)
all_routers.include_router(user_router)
