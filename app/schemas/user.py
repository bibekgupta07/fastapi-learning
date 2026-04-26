# This represents data coming IN from requests and going OUT in responses

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

# ── What the client sends to REGISTER ──
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if len(v) > 72:
            raise ValueError("Password must not exceed 72 characters")
        return v

# ── What the client sends to LOGIN ──
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# ── What we SEND BACK to client (never include password!) ──
class UserResponse(BaseModel):
    email: EmailStr
    username: str
    is_active: bool

# ── JWT Token response ──
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
# ── Forgot password request ──
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

# ── Reset password request ──
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
