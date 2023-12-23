from typing import List, Optional

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func

from sqlalchemy.orm import Session

from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/",  response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    posts = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).
             join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).
             group_by(models.Post.id).filter(models.Post.title.contains(search)).
             offset(skip).limit(limit).all())
    # result = list(map(lambda x:x._mapping, query))

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **dict(post))  # create entry
    db.add(new_post)  # add entry to DB
    db.commit()  # commit changes
    db.refresh(new_post)   # RETURNING *
    return new_post


@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} was not found!")
    elif post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to action")


    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == post_id)
    post = query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {post_id} was not found!")
    elif post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to action")

    query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == post_id)
    updated_post = query.first()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {post_id} was not found!")
    elif updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to action")


    query.update(dict(post))
    db.commit()
    return query.first()
