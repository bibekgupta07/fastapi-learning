from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # These are read from your .env file automatically
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "myapp"
    
    SECRET_KEY: str = "your-secret-key-change-this"  # Used to sign JWT tokens
    ALGORITHM: str = "HS256"                          # JWT signing algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30             # Token expiry
    
    class Config:
        env_file = ".env"  # Tells pydantic to read from .env

# Create one global instance — import this everywhere
settings = Settings()
  
  
