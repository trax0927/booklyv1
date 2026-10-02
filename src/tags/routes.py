from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.auth.dependencies import RoleChecker
from src.books.schemas import Book

from .schemas import TagCreateModel, TagAddModel, TagModel
from .service import TagsService

tags_router = APIRouter()
tags_service = TagsService()
user_role_check = Depends(RoleChecker(["user", "admin"]))

@tags_router.get("/", response_model=List[TagModel], dependencies=[user_role_check])
async def get_all_tags(session: AsyncSession = Depends(get_session)):
    
    tags = await tags_service.get_all_tags(session)
    
    return tags

@tags_router.post("/", response_model=TagModel, dependencies=[user_role_check])
async def create_a_tag(tag_data: TagCreateModel, session: AsyncSession = Depends(get_session)):
    
    tag = await tags_service.create_tag(tag_data, session)
    
    return tag

@tags_router.post("/book/{book_uid}/tags", response_model=Book, dependencies=[user_role_check])
async def add_tags_to_book(book_uid: str, tag_data: TagAddModel, session: AsyncSession = Depends(get_session)):
    
    book_with_tags = await tags_service.add_tags_to_book(book_uid, tag_data, session)
    
    return book_with_tags

@tags_router.patch("/{tag_uid}", response_model=TagModel, dependencies=[user_role_check])
async def update_a_tag(tag_uid: str, tag_data: TagCreateModel, session: AsyncSession = Depends(get_session)):
    
    updated_tag = await tags_service.update_tag(tag_uid, tag_data, session)
    
    return updated_tag

@tags_router.delete("/{tag_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[user_role_check])
async def delete_tag(tag_uid: str, session: AsyncSession = Depends(get_session)):
    
    deleted_tag = await tags_service.delete_tag(tag_uid, session)

    return deleted_tag