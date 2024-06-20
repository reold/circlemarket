from fastapi import APIRouter

router = APIRouter(prefix="/inventory")

@router.get("/get")
def login():
    return "inventory items..."

@router.get("/append")
def signup():
    return "add item to inventory"

@router.get("/modify")
def signup():
    return "modified inventory item"

@router.get("/remove")
def signup():
    return "removed inventory item"