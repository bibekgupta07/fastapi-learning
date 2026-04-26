# This is used to PROTECT routes — only logged in users can access them

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from app.db.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

security = HTTPBearer()  # Reads "Bearer <token>" from Authorization header

async def get_current_user(
  credentials: HTTPAuthorizationCredentials = Depends(security),
  db: AsyncIOMotorDatabase = Depends(get_database)
):
  """
    Use this as a dependency on any route that requires login.
    Example: async def my_route(user = Depends(get_current_user))
    """
  token = credentials.credentials
  email = decode_access_token(token)
  
  if not email:
    raise HTTPException(
      status_code= status.HTTP_401_UNAUTHORIZED,
      detail="Invalid or expired token"
    )
    
  user = await db["users"].find_one({"email": email})
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
    
    return user