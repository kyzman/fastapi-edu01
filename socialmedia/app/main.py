from fastapi import FastAPI

from app.routers.post import router as post_router
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.vote import router as vote_router

app = FastAPI()

app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(vote_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
