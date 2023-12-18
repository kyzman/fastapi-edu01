from typing import Optional

from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='socialmedia',
                                user='postgres', password='loop', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connect successful!")
        break
    except Exception as error:
        print("DB connection failed!")
        print("Error:", error)
        time.sleep(3)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
                   (new_post.title, new_post.content, new_post.published))  # don't use f-string to avoid sql injection
    post = cursor.fetchall()
    conn.commit()
    return {"new_post": f"new post created", "data": post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found!")

    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} was not found!")

    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title,post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} was not found!")

    return {"data": updated_post}

