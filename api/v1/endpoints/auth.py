import re
from fastapi import APIRouter, HTTPException, Depends, Request, status, Response
from sqlalchemy.orm import Session
from core.database import SessionLocal
from core.security import create_jwt_token, create_refresh_token, verify_refresh_token, verify_token, hash_password, verify_password
from models.user import User
from schemas.user import LoginRequest, TokenResponse, UserCreate, UserResponse


router = APIRouter()

# Fonction de validation du mot de passe
def validate_password(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password should contains at least 8 characters .")
    if not any(c.isupper() for c in password):
        raise ValueError("Password should contains at least 1 uppercased character.")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password should contains at least 1 number.")
    if not any(c in "@$!%*?&" for c in password):
        raise ValueError("Password should contains at least 1 special character (@$!%*?&).")
    return password

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi import HTTPException, status  # Import HTTPException and status

@router.post("/login")  
async def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    db.expire_all() 
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="credentials_invalid")

    token = create_jwt_token(user.email, user.role)
    refresh_token = create_refresh_token(user.email, user.role)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=1800,
    )
    response.set_cookie(key="access_token", value=token, httponly=True, secure=True, samesite="Strict")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="Strict")

    return {"isAuthenticated": True, "role": user.role, "user": user.email} 

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="user_already_exists")

    hashed_password = hash_password(user_data.password)
    new_user = User(email=user_data.email, password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_jwt_token(new_user.email, new_user.role)
    return UserResponse(id=new_user.id, email=new_user.email, role=new_user.role, token=TokenResponse(access_token=token, token_type="Bearer"))

@router.get("/is-logged-in")
def protected_route(user: dict = Depends(verify_token)):
    return {"isAuthenticated": True, "role": user['role'], "user": user['sub']}

@router.post("/refresh-token")
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token") 

    if not refresh_token:
        print("Refresh toke missing") 
        raise HTTPException(status_code=403, detail="refresh_token_missing")

    try:
        user = verify_refresh_token(refresh_token)
    except Exception as e:
        print(f"Refresh Token invalid: {e}")
        raise
    
    new_access_token = create_jwt_token(user["sub"], user["role"])
    response.set_cookie(key="access_token", value=new_access_token, httponly=True, secure=True, samesite="Strict")
    return {"isAuthenticated": True, "role": user['role'], "user": user['sub']}