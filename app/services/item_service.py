from typing import Any
from app.schemas.item import ItemCreate, ItemUpdate
from datetime import datetime, timezone
from bson import ObjectId  # MongoDB uses ObjectId for _id

# ── helper: convert MongoDB doc → clean dict ──
def item_to_dict(item: dict) -> dict:
  """
    MongoDB stores _id as ObjectId e.g. ObjectId("507f1f77...")
    We convert it to a plain string so JSON can serialize it
    """
  item["id"] = str(item["id"])  #ObjectId -> string
  del item["_id"]               # remove original _id
  # convert datetimes to string
  item["created_at"] = str(item["created_at"])
  item["updated_at"] = str(item["updated_at"])
  return item

# ── CREATE ──
async def create_item(item_data: ItemCreate, owner_email: str, db: Any):
  """
    1. Build the document
    2. Insert into MongoDB
    3. Return created item
    """
  now = datetime.now(timezone.utc)
  
  item_doc = {
    "title": item_data.title,
    "description": item_data.description,
    "price": item_data.price,
    "is_available": True,
    "owner_email": owner_email,   # from JWT — who is logged in
    "created_at": now,
    "updated_at": now,
  }
  
  result = await db["items"].insert_one(item_doc)
  
  # fetch the inserted doc to return it
  created = await db["items"].find_one({"_id": result.inserted_id})
  return item_to_dict(created)


# ── READ ALL ──
async def get_all_items(db: Any):
    """
    Fetch every item from DB
    MongoDB returns a cursor — we loop through it to build a list
    """
    cursor = db["items"].find()        # cursor = like a pointer, not data yet
    items = []
    async for item in cursor:          # await each item as it streams
        items.append(item_to_dict(item))
    return items
  

# ── READ ONE ──
async def get_item_by_id(item_id: str, db: Any):
    """
    1. Convert string id → ObjectId (MongoDB needs this)
    2. Find the document
    3. Return it or raise error
    """
    try:
        obj_id = ObjectId(item_id)    # "507f1f77..." → ObjectId("507f1f77...")
    except Exception:
        raise ValueError("Invalid item ID format")

    item = await db["items"].find_one({"_id": obj_id})

    if not item:
        raise ValueError("Item not found")

    return item_to_dict(item)
  
  
  # ── UPDATE ──
async def update_item(item_id: str, item_data: ItemUpdate, owner_email: str, db: Any):
    """
    1. Check item exists
    2. Check it belongs to this user
    3. Build update dict (only fields that were sent)
    4. Update in MongoDB
    """
    try:
        obj_id = ObjectId(item_id)
    except Exception:
        raise ValueError("Invalid item ID format")

    item = await db["items"].find_one({"_id": obj_id})

    if not item:
        raise ValueError("Item not found")

    if item["owner_email"] != owner_email:
        raise PermissionError("You can only update your own items")

    # Only update fields that were actually sent (not None)
    update_fields = {
        k: v for k, v in item_data.model_dump().items() if v is not None
    }
    update_fields["updated_at"] = datetime.now(timezone.utc)

    await db["items"].update_one(
        {"_id": obj_id},
        {"$set": update_fields}        # $set = only update these fields
    )

    updated = await db["items"].find_one({"_id": obj_id})
    return item_to_dict(updated)
  
  
  # ── DELETE ──
async def delete_item(item_id: str, owner_email: str, db: Any):
    """
    1. Check item exists
    2. Check it belongs to this user
    3. Delete it
    """
    try:
        obj_id = ObjectId(item_id)
    except Exception:
        raise ValueError("Invalid item ID format")

    item = await db["items"].find_one({"_id": obj_id})

    if not item:
        raise ValueError("Item not found")

    if item["owner_email"] != owner_email:
        raise PermissionError("You can only delete your own items")

    await db["items"].delete_one({"_id": obj_id})

    return {"message": f"Item '{item['title']}' deleted successfully"}