from pydantic import BaseModel, field_validator
from typing import Optional

# ── CLIENT SENDS THIS TO CREATE ──
class ItemCreate(BaseModel):
  title: str
  description: Optional[str] = None
  price: float
  
  @field_validator("price")
  @classmethod
  def price_must_be_positive(cls, v):
    if v <= 0:
      raise ValueError("Price must be greater than 0")
    return v
  
  @field_validator("title")
  @classmethod
  def title_must_not_be_empty(cls, v):
    if not v.strip():
      raise ValueError("Title cannot be empty")
    return v
  
  
# ── CLIENT SENDS THIS TO UPDATE ──
class ItemUpdate(BaseModel):
  title: Optional[str] = None  # all fields optional
  description: Optional[str] = None # client sends only what changed
  price: Optional[float] = None
  is_available: Optional[bool] = None
  

# ── SERVER SENDS THIS BACK ──
class ItemResponse(BaseModel):
    id: str                           # MongoDB _id converted to string
    title: str
    description: Optional[str] = None
    price: float
    is_available: bool
    owner_email: str
    created_at: str
    updated_at: str
    
  