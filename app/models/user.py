# This represents how a user is stored IN MongoDB

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timezone

class UserInDB(BaseModel):
  """This is what actually goes into the database"""
  email: EmailStr
  username: str
  hashed_password: str
  is_active: bool = True
  created_at: datetime = datetime.now(timezone.utc)
  reset_token: Optional[str] = None
  reset_token_expires: Optional[datetime] = None