from fastapi import APIRouter

router = APIRouter(prefix="/feed")

@router.get("/generate")
def login():
    return "generated feed"
