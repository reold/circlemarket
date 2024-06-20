from fastapi import FastAPI

from .router import account, feed, inventory

app = FastAPI()

app.include_router(account.router, prefix="/api")
app.include_router(feed.router, prefix="/api")
app.include_router(inventory.router, prefix="/api")

@app.get("/")
def root():
    return "Welcome to marketplace!"
