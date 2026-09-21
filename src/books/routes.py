from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.books.schemas import Book, UpdateBookModel, BookCreateModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from .service import BookService
from .models import Book
from typing import List
from src.auth.dependencies import AccessTokenBearer

book_router = APIRouter()
book_service = BookService()
accessToken_bearer = AccessTokenBearer()

@book_router.get('/', response_model=List[Book])
async def get_books(session:AsyncSession = Depends(get_session), user_details=Depends(accessToken_bearer)) -> List[Book]:
    print("user details", user_details)
    books = await book_service.get_all_books(session)
    return books

@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book_data:BookCreateModel, session:AsyncSession = Depends(get_session), user_details=Depends(accessToken_bearer)) -> dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book
    
@book_router.get('/{book_uid}')
async def get_books(book_uid:str, session:AsyncSession = Depends(get_session), user_details=Depends(accessToken_bearer)) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book:
        return book 
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "book not found")

@book_router.patch('/{book_uid}', response_model=UpdateBookModel)
async def update_book(book_uid: str, book_update_data:UpdateBookModel, session:AsyncSession = Depends(get_session), user_details=Depends(accessToken_bearer)) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if updated_book:
        return updated_book
    else:    
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "book not found")


@book_router.delete('/{book_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid:str, session:AsyncSession = Depends(get_session), user_details=Depends(accessToken_bearer)):
    book_to_delete = await book_service.delete_book(book_uid, session)
    if book_to_delete:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "book not found")

