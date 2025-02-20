from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from core.security import decode_jwt_token

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/protected"):
            authorization: str = request.headers.get("Authorization")
            if not authorization:
                raise HTTPException(status_code=401, detail="access_token_missing")

            try:
                token = authorization.split("Bearer ")[1]
                decode_jwt_token(token)
            except IndexError:
                raise HTTPException(status_code=401, detail="access_token_invalid")

        return await call_next(request)