from pydantic import BaseModel
import uuid
from datetime import datetime

class TagModel(BaseModel):
    uid: uuid.UUID
    book_uid: uuid.UUID
    name: str
    created_at: datetime

class TagCreateModel(BaseModel):
    name: str

class TagAddModel(BaseModel):
    tags: list[TagCreateModel]