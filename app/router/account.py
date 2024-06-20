from fastapi import APIRouter

router = APIRouter(prefix="/account")

@router.get("/signup")
def signup():
    return "signup"

@router.get("/login")
def login():
    return "login"
