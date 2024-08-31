from fastapi import APIRouter

from src.api.routes import groups
from src.api.routes import expenses

app_router = APIRouter()
app_router.include_router(groups.router, prefix="/groups", tags=["groups"])
app_router.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
