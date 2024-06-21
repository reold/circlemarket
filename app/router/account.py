from fastapi import APIRouter

from pydantic import BaseModel, Field
from hashlib import sha256
from uuid import uuid4 as uuid
import time

from app.db import user_db, inventory_db
from app.resp import respond

router = APIRouter(prefix="/account")

ACCESS_TOKEN_VALIDITY_SECONDS = 604800

class SignupInfo(BaseModel):
    email: str
    password: str = Field(min_length=8)
    username: str = Field(min_length=3)

class AccountInfo(SignupInfo):
    description: str = ""
    picture_key: str = ""
    rating: int = Field(0, min=0, max=5)
    rating_count: int = Field(0, min=0)
    inventory_key: str
    access_tokens: list = []

class LoginInfo(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(info: SignupInfo):

    if user_db.fetch({"username":  info.username}).count > 0:
        return respond({}, False, "username-taken")
    
    if user_db.fetch({"email":  info.email}).count > 0:
        return respond({}, False, "email-in-use")

    info.password = sha256(info.password.encode("utf-8")).hexdigest()

    inventory = inventory_db.put({"username": info.username})
    access_token = uuid().hex
    
    acc = AccountInfo(**info.model_dump(), inventory_key=inventory["key"], access_tokens=[
        {"token": access_token, "validity": str(time.time() + ACCESS_TOKEN_VALIDITY_SECONDS)}]
    )
    
    user_db.put(acc.model_dump())

    client_access_token = f"{info.username}@{access_token}"

    return respond({"access_token": client_access_token})


@router.post("/login")
async def login(info: LoginInfo):

    acc_resp = user_db.fetch({"email": info.email})

    if acc_resp.count == 0:
        return respond({}, False, "account-not-found")
    
    acc_info = acc_resp.items[0]
    passhash = sha256(info.password.encode("utf-8")).hexdigest()

    if acc_info["password"] == passhash:
        access_token = uuid().hex
        
        user_db.update({"access_tokens": user_db.util.append({"token": access_token, "validity": str(time.time() + ACCESS_TOKEN_VALIDITY_SECONDS)})}, acc_info["key"])

        client_access_token = f"{acc_info["username"]}@{access_token}"

        return respond({"access_token": client_access_token})
    else:
        return respond({}, False, "inncorrect-password")
