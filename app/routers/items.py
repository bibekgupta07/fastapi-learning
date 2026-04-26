from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services import item_service
from app.db.database import get_database
from app.dependencies import get_current_user  # ← protects all routes

router = APIRouter(prefix="/items", tags=["Items"])


# ── CREATE ──────────────────────────────────────────
@router.post("/", status_code=201)
async def create_item(
    item_data: ItemCreate,
    db: Any = Depends(get_database),
    current_user: dict = Depends(get_current_user)  # must be logged in
):
    try:
        return await item_service.create_item(item_data, current_user["email"], db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── READ ALL ─────────────────────────────────────────
@router.get("/")
async def get_all_items(
    db: Any = Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    return await item_service.get_all_items(db)


# ── READ ONE ─────────────────────────────────────────
@router.get("/{item_id}")
async def get_item(
    item_id: str,                       # FastAPI reads this from the URL
    db: Any = Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    try:
        return await item_service.get_item_by_id(item_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── UPDATE ───────────────────────────────────────────
@router.put("/{item_id}")
async def update_item(
    item_id: str,
    item_data: ItemUpdate,
    db: Any = Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    try:
        return await item_service.update_item(item_id, item_data, current_user["email"], db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# ── DELETE ───────────────────────────────────────────
@router.delete("/{item_id}")
async def delete_item(
    item_id: str,
    db: Any = Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    try:
        return await item_service.delete_item(item_id, current_user["email"], db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))