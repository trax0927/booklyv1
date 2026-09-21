from  pydantic import BaseModel
import uuid
import datetime

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    pages: int 
    genre: str 
    published_date: datetime.date  
    rating: float
    created_at: datetime.datetime
    update_at: datetime.datetime

class BookCreateModel(BaseModel):
    title: str
    author: str
    pages: int
    genre: str 
    published_date: datetime.date 
    rating: float  

class UpdateBookModel(BaseModel):
    title: str
    author: str
    pages: int 
    rating: float 