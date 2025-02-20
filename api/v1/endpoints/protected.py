from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_jwt_token, verify_token
from middlewares.role_middleware import require_role

router = APIRouter()
security = HTTPBearer()

@router.get("/hello")
async def protected_route(user: dict = Depends(verify_token)):
    return {"message": f"Bienvenue {user['sub']}!"}

@router.get("/admin", dependencies=[Depends(require_role("admin"))])
async def admin_only():
    return {"message": "Bienvenue, Admin !"}