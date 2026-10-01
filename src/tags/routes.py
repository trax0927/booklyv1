from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.auth.dependencies import RoleChecker
from src.books.schemas import Book

from .schemas import TagCreateModel, TagAddModel, TagModel
from .service import TagsService

tags_router = APIRouter()
tags_service = TagsService()

@tags_router.get("/")
async def get_all_tags():
    pass

@tags_router.post("/")
async def create_a_tag():
    pass

@tags_router.post("/{book_uid}")
async def add_tags_to_book(book_uid: str):
    pass

@tags_router.patch("/{tag_uid}")
async def update_a_tag(tag_uid: str):
    pass

@tags_router.delete("/{tag_uid}")
async def delete_tag(tag_uid: str):
    pass