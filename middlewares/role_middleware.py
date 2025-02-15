from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_jwt_token

security = HTTPBearer()

def require_role(required_role: str):
    def role_checker(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        user_data = decode_jwt_token(token)
        
        
        if 'role' not in user_data or user_data["role"] != required_role:
            raise HTTPException(status_code=403, detail="Forbidden access")

        return user_data
    return role_checker