from fastapi import APIRouter

from src.api.routes import groups

app_router = APIRouter()
app_router.include_router(groups.router, prefix="/groups", tags=["groups"])
