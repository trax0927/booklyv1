from  pydantic import BaseModel
import uuid
from datetime import datetime, date

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    pages: int 
    genre: str 
    published_date: date  
    rating: float
    created_at: datetime
    update_at: datetime

class BookCreateModel(BaseModel):
    title: str
    author: str
    pages: int
    genre: str 
    published_date: str 
    rating: float  

class UpdateBookModel(BaseModel):
    title: str
    author: str
    pages: int 
    rating: float 