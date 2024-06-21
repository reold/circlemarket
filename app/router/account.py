from fastapi import APIRouter

from pydantic import BaseModel, Field
from hashlib import sha256

from app.db import user_db, inventory_db
from app.resp import respond

router = APIRouter(prefix="/account")

class SignupInfo(BaseModel):
    email: str
    password: str = Field(min_length=8)
    username: str = Field(min_length=3)

class AccountInfo(SignupInfo):
    description: str = ""
    picture_key: str = ""
    inventory_key: str

class LoginInfo(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(info: SignupInfo):

    if user_db.fetch({"username":  info.username}).count > 0:
        return respond({}, False, "username-taken")

    info.password = sha256(info.password.encode("utf-8")).hexdigest()

    inventory = inventory_db.put({"username": info.username})
    
    acc = AccountInfo(**info.model_dump(), inventory_key=inventory["key"])
    
    user_db.put(acc.model_dump())

    return respond({})

@router.post("/login")
async def login(info: LoginInfo):

    acc_resp = user_db.fetch({"email": info.email})

    if acc_resp.count == 0:
        return respond({}, False, "account-not-found")
    
    acc_info = acc_resp.items[0]
    passhash = sha256(info.password.encode("utf-8")).hexdigest()

    if acc_info["password"] == passhash:
        return respond({})
    else:
        return respond({}, False, "inncorrect-password")

