
from sqlalchemy.orm import Session

from fastapi import status, HTTPException, Depends, APIRouter

from app.database import get_db
from app import models, schemas, utils


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash_pwd(user.password)
    new_user = models.User(**dict(user))  # create entry
    db.add(new_user)  # add entry to DB
    db.commit()  # commit changes
    db.refresh(new_user)   # RETURNING *
    return new_user


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {user_id} was not found!")

    return user
