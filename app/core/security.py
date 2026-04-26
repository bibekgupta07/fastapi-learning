from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from app.core.config import settings

# bcrypt is the hashing algorithm — industry standard
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
  """Turns 'mypassword123' → '$2b$12$...' (unreadable hash)"""
  return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
  """Checks if plain password matches the stored hash"""
  return pwd_context.verify(plain_password, hashed_password)

# ── JWT Token Functions ──
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  """
  Create a Jwt token.
  data = {"sub":"user@email.com"} 'sub' means subject (who the token is for)
  """
  to_encode = data.copy()
  
  expire = datetime.utcnow() + (
    expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  )
  to_encode.update({"exp": expire})  # Add expiry to token payload
  
  # Sign the token with our secret key
  return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
  """
  Decodes a JWT token and returns the email (subject).
  Returns None if token is invalid or expired.
  """
  try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return payload.get("sub")
  except JWTError: 
    return None
    