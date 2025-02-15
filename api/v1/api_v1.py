from fastapi import APIRouter
from api.v1.endpoints import example, auth, protected

api_router = APIRouter()
api_router.include_router(example.router, prefix="/example")
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(protected.router, prefix="/protected")