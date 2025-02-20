from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_jwt_token

security = HTTPBearer()

def require_role(required_role: str):
    def role_checker(request: Request): 
        token = request.cookies.get("access_token")
        user_data = decode_jwt_token(token)
        print('USER', user_data)
        if 'role' not in user_data or user_data["role"] != required_role:
            raise HTTPException(status_code=403, detail="insufficient_permissions")

        return user_data
    return role_checker