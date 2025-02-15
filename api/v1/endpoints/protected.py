from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_jwt_token
from middlewares.role_middleware import require_role

router = APIRouter()
security = HTTPBearer()

@router.get("/hello")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_data = decode_jwt_token(token)
    return {"message": f"Bienvenue {user_data['sub']}!"}

@router.get("/admin", dependencies=[Depends(require_role("admin"))])
async def admin_only():
    return {"message": "Bienvenue, Admin !"}