from fastapi import HTTPException, status

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc, func
from src.db.models import Tag
from .schemas import TagCreateModel, TagAddModel

from src.books.service import BookService

book_service = BookService()

class TagsService:
    async def get_all_tags(self, session: AsyncSession):

        statement = select(Tag).order_by(desc(Tag.created_at))
        result = await session.exec(statement)

        tags = result.all()

        return tags

    async def create_tag(self, tag_data: TagCreateModel, session: AsyncSession):

        statement = select(Tag).where(func.lower(Tag.name) == tag_data.name.strip().lower())
        result = await session.exec(statement)

        tag = result.first()
        if tag:
            raise HTTPException(status_code=400, detail="Tag already exists")

        new_tag = Tag(name=tag_data.name.strip())

        session.add(new_tag)
        await session.commit()

        return new_tag

    async def get_tag_by_uid(self, tag_uid: str, session: AsyncSession):

        statement = select(Tag).where(Tag.uid == tag_uid)
        result = await session.exec(statement)

        return result.first()

    async def add_tags_to_book(self, book_uid: str, tag_data: TagAddModel, session: AsyncSession):

        book = await book_service.get_book(book_uid, session)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

        for tag_info in tag_data.tags:
            statement = select(Tag).where(func.lower(Tag.name) == tag_info.name.strip().lower())
            result = await session.exec(statement)
            tag = result.one_or_none()

            if not tag:
                tag = Tag(name=tag_info.name.strip())

            if tag not in book.tags:
                book.tags.append(tag)

        session.add(book)
        await session.commit()
        await session.refresh(book)

        return book

    async def update_tag(self, tag_uid: str, tag_data: TagCreateModel, session: AsyncSession):

        statement = select(Tag).where(Tag.uid == tag_uid)
        result = await session.exec(statement)

        tag_to_update = result.first()

        if not tag_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

        tag_to_update.name = tag_data.name

        session.add(tag_to_update)
        await session.commit()
        await session.refresh(tag_to_update)

        return tag_to_update

    async def delete_tag(self, tag_uid: str, session: AsyncSession):
        tag_to_delete = await self.get_tag_by_uid(tag_uid, session)

        if tag_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

        await session.delete(tag_to_delete)
        await session.commit()

        return True
