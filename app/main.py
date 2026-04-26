from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import connect_to_mongo, close_mongo_connection
from app.routers import users, items

# Lifespan handles startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()   # ← runs on startup
    yield
    await close_mongo_connection()  # ← runs on shutdown

app = FastAPI(title="My App", lifespan=lifespan)

# Register routers
app.include_router(users.router)
app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "API is running"}