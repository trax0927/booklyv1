from  pydantic import BaseModel, Field
import uuid
from datetime import datetime, date

class ReviewModel(BaseModel):
    uid: uuid.UUID
    book_uid: uuid.UUID
    user_uid: uuid.UUID
    rating: float = Field(le=10)
    comment: str
    created_at: datetime
    update_at: datetime

class ReviewCreateModel(BaseModel):
    rating: float = Field(le=10)
    comment: str  