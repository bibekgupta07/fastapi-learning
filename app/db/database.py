from motor.motor_asyncio import AsyncIOMotorClient   # Async MongoDB driver
from app.core.config import settings   # ← imports from config.py

client = None
database = None

async def connect_to_mongo():
  """Called when app starts"""
  global client, database
  client = AsyncIOMotorClient(settings.MONGODB_URL)
  database = client[settings.DATABASE_NAME]
  print("Connected to MongoDB")
  
async def close_mongo_connection():
  """Called when app shuts down"""
  global client
  if client:
    client.close()
    print("Disconnected from MongoDB")
    
def get_database():
  """Used as a dependency in routes"""
  return database