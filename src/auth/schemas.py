from  pydantic import BaseModel, Field
from src.books.schemas import Book
from typing import List
import uuid
from datetime import datetime

class UserCreateModel(BaseModel):
    username: str = Field(min_length=3, max_length=10)
    email: str = Field(min_length=10)
    password: str = Field(min_length=6)
    first_name: str
    last_name: str

class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    update_at: datetime
    books: List[Book]

class UserLoginModel(BaseModel):
    email: str = Field(min_length=10)
    password: str = Field(min_length=6)