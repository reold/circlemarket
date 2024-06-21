from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .router import account, feed, inventory

app = FastAPI()

# CORS setup
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True)

# router setup
app.include_router(account.router, prefix="/api")
app.include_router(feed.router, prefix="/api")
app.include_router(inventory.router, prefix="/api")

@app.get("/")
def root():
    return "Welcome to marketplace!"