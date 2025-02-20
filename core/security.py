import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

SECRET_KEY = "my_secret_key"
REFRESH_SECRET_KEY = "superrefreshsecretkey"
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 1 
REFRESH_TOKEN_EXPIRATION_DAYS = 2  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_jwt_token(user_id: str, role: str) -> str:
    expiration = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    payload = {"sub": user_id, "role": role, "exp": expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return payload 
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="access_token_expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="access_token_invalid")
    
def create_refresh_token(user_id: str, role: str):
    expiration = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRATION_DAYS)
    expiration = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRATION_DAYS)

    payload = {"sub": user_id, "role": role, "exp": expiration}
    return jwt.encode(payload, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    
def verify_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="access_token_missing")

    return decode_jwt_token(token)

def verify_refresh_token(token: str):

    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="refresh_token_expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="refresh_token_invalid")