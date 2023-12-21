from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers.post import router as post_router
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
