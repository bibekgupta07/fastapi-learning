# This is the BRAIN of authentication — all logic lives here

from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.user import UserRegister, UserLogin
from app.models.user import UserInDB
from app.core.security import hash_password, verify_password, create_access_token
from datetime import datetime, timedelta, timezone
import secrets  #For generating reset token

async def register_user(user_data: UserRegister, db: AsyncIOMotorDatabase):
  """
   Flow:
    1. Check if email already exists
    2. Hash the password
    3. Save to MongoDB
    4. Return the created user
  """
  # Step 1: Check duplicate email
  existing = await db["users"].find_one({"email": user_data.email})
  if existing:
    raise ValueError("Email already registered")
  
  # Step 2:  Hash password - Never save plain text
  hashed = hash_password(user_data.password)
  
  # Step 3: Build the DB document
  user_doc = {
    "email": user_data.email,
    "username": user_data.username,
    "hashed_password": hashed,
    "is_active": True,
    "created_at": datetime.now(timezone.utc)
  }
  
  # Step 4: Insert into MongoDB
  await db["users"].insert_one(user_doc)
  return {"email": user_data.email, "username": user_data.username}

async def login_user(user_data: UserLogin, db: AsyncIOMotorDatabase):
  """
    Flow:
    1. Find user by email
    2. Verify password
    3. Create JWT token
    4. Return token
  """
  # Step 1: Find user
  user = await db["users"].find_one({"email":user_data.email})
  if not user:
    raise ValueError("Invalid email or password")   # Vague on purpose (security)
  
  # Step 2: Check password
  if not verify_password(user_data.password, user["hashed_password"]):
    raise ValueError("Invalid email or password")
  
  # Step 3: Create JWT
  token = create_access_token(data={"sub": user["email"]})
  
  return {"access_token": token, "token_type": "bearer"}


async def forget_password(email: str, db: AsyncIOMotorDatabase):
  """
    Flow:
    1. Check if email exists
    2. Generate a reset token
    3. Save token + expiry to DB
    4. (In real app: send email — skipped here)
    """
  user = await db["users"].find_one({"email": email})
  if not user:
       # Don't reveal if email exists — security best practice
       return {"message": "If email exists, reset link was sent"}
     
  # Generate secure random token
  reset_token = secrets.token_urlsafe(32)
  expires = datetime.now(timezone.utc) + timedelta(hours=1)
  
  # Save to DB
  await db["users"].update_one(
    {"email": email},
    {"$set":{"reset_token": reset_token, "reset_token_expires": expires}}
  )
  
  # In production: send email with reset link containing the token
  # For now, return it directly (for testing)
  return {"message": "Reset token generated", "reset_token": reset_token}

async def reset_password(token: str, new_password: str, db: AsyncIOMotorDatabase):
  """
    Flow:
    1. Find user by reset token
    2. Check token hasn't expired
    3. Hash new password and save
    4. Clear the reset token
    """
  user = await db["users"].find_one({"reset_token": token})
  
  if not user:
    raise ValueError("Invalid reset token")
  
  # Make the stored datetime timezone-aware if it isn't already
  token_expires = user["reset_token_expires"]
  if token_expires.tzinfo is None:
    token_expires = token_expires.replace(tzinfo=timezone.utc)
  
  if token_expires < datetime.now(timezone.utc):
    raise ValueError("Reset token has expired")
  
  # Hash and save new password, clear reset token
  await db["users"].update_one(
    {"reset_token": token},
    {"$set":{
      "hashed_password": hash_password(new_password),
      "reset_token": None,
      "reset_token_expires": None
    }}
  )
  
  return {"message": "Password updated successfully"}
      
  
  