from  pydantic import BaseModel
import uuid
from datetime import datetime, date
from src.reviews.schema import ReviewModel
from typing import List

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    pages: int 
    genre: str 
    published_date: date
    created_at: datetime
    update_at: datetime

class BookDetailModel(Book):
    reviews: List[ReviewModel]

class BookCreateModel(BaseModel):
    title: str
    author: str
    pages: int
    genre: str 
    published_date: str 

class UpdateBookModel(BaseModel):
    title: str
    author: str
    pages: int 
