from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemInDB(BaseModel):
  """Exactly what gets stored in MongoDB"""
  title: str
  description: Optional[str] = None
  price: float
  is_available: bool = True
  owner_email: str     # which user owns this item
  created_at: datetime
  updated_at: datetime