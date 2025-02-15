from pydantic import BaseModel, ConfigDict, EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    token: TokenResponse

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
