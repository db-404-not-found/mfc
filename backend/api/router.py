from fastapi import APIRouter

from backend.api import monitoring
from backend.api.v1.router import router as v1_router

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(v1_router)
