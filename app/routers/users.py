# This is what the clients hits - thin layer, just calls services

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.user import UserRegister, UserLogin, Token, ForgotPasswordRequest, ResetPasswordRequest
from app.services import user_service
from app.db.database import get_database

router = APIRouter(prefix="/auth", tags=["Authentication"])
#                  ↑ all routes here start with /auth

@router.post("/register", status_code=201)
async def register(user_data: UserRegister, db: AsyncIOMotorDatabase = Depends(get_database)):
  """
    Depends(get_database) → FastAPI automatically injects the DB connection
    """
  try:
    result = await user_service.register_user(user_data, db)
    return result
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
  
@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        result = await user_service.login_user(user_data, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/forget-password")
async def forget_password(request: ForgotPasswordRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
  result = await user_service.forget_password(request.email, db)
  return result

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        result = await user_service.reset_password(request.token, request.new_password, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 
  