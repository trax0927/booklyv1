from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import BookCreateModel, UpdateBookModel 
from sqlmodel import select, desc
from .models import Book
from datetime import datetime

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        books = result.all()
        return books

    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        return book if book else None

    async def create_book(self, book_data: BookCreateModel, user_uid: str,session: AsyncSession):
        new_book = Book(**book_data.model_dump())
        new_book.published_date = datetime.strptime(book_data.published_date, "%Y-%m-%d").date()
        
        new_book.user_uid = user_uid  # Associate the book with the user who created it
        session.add(new_book)
        await session.commit()

        return new_book

    async def update_book(self, book_uid: str, update_data: UpdateBookModel, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book_to_update = result.first()

        if book_to_update is None:
            return None

        update_data_dict = update_data.model_dump()

        for k, v in update_data_dict.items():
            setattr(book_to_update, k, v)

        await session.commit()
        
        return book_to_update
            

    async def delete_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book_to_delete = result.first()

        if book_to_delete is None:
            return None
        
        await session.delete(book_to_delete)
        await session.commit()

    async def get_user_books(self, user_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.user_uid == user_uid).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        books = result.all()
        return books