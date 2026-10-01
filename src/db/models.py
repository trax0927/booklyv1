from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
from typing import Optional, List
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
            info={"description": "Unique identifier for the user account"},
        )
    ) 
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(pg.VARCHAR, server_default="user", nullable=False))
    password_hash: str = Field(exclude=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))
    books: List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    reviews: List["Review"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"})

    def __repr__(self):
        return f"<User {self.username}>"


class BookTag(SQLModel, table=True):
    book_uid: uuid.UUID = Field(default=None, foreign_key="books.uid", primary_key=True)
    tag_uid: uuid.UUID = Field(default=None, foreign_key="tags.uid", primary_key=True)

class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    title: str
    author: str
    pages: int 
    language: str 
    published_date: date
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"})
    tags: List["Tag"] = Relationship(
        link_model=BookTag,
        back_populates="books",
        sa_relationship_kwargs={"lazy": "selectin"}
        )

    def __repr__(self):
        return f"<Book {self.title}>"

class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))
    books: List["Book"] = Relationship(
        link_model=BookTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy": "selectin"}
        )

    def __repr__(self):
        return f"<Tag {self.name}>"

class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    book_uid: uuid.UUID = Field(default=None, foreign_key="books.uid")
    user_uid: uuid.UUID = Field(default=None, foreign_key="users.uid")
    rating: float = Field(lt=10.0, gt=0.0)
    comment: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))
    update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, nullable=False))
    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for {self.book_uid} by {self.user_uid}>"