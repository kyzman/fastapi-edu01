from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post1", "content": "content of post1", "id": 1},
            {"title": "favorite food", "content": "I like pizza", "id": 2},
            {"title": "title of post3", "content": "content of post3", "id": 3}]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(new_post: Post):
    post = dict(new_post)
    post['id'] = randrange(0,1000000)
    my_posts.append(post)
    return {"new_post": f"new post received", "data" : post}
