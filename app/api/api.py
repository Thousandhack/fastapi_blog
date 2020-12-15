from fastapi import APIRouter
from app.api.endpoints import base

api_router = APIRouter()
api_router.include_router(base.router, tags=['base'])


