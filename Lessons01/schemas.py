from typing import List

from pydantic import BaseModel, field_validator, Field
from datetime import date


class Genre(BaseModel):
    name: str


class Author(BaseModel):
    first_name: str = Field(..., max_length=25)
    last_name: str
    age: int = Field(..., gt=15, lt=90, description='Author age must be more than 15 an less than 90')

    # @field_validator('age')
    # @classmethod
    # def check_age(cls, v):
    #     if (v < 15) or (v > 90):
    #         raise ValueError('Author age must be more than 15 an less than 90')
    #     return v


class Book(BaseModel):
    title: str
    writer: str
    duration: str
    date: date
    summary: str
    genres: List[Genre]
    pages: int
