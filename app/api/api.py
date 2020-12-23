from fastapi import APIRouter
from app.api.endpoints import base
from app.api.blog import blog

api_router = APIRouter()
api_router.include_router(base.router, tags=['auth'], prefix='/auth')
api_router.include_router(blog.router, tags=['blog'], prefix='/blog')