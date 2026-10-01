import logging

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from src.db.models import Review
from .schema import ReviewCreateModel
from src.auth.service import UserService
from src.books.service import BookService
from fastapi import HTTPException, status


book_service = BookService()
user_service = UserService()

class ReviewService:

    async def add_review(self, user_email: str, book_uid: str, review_data: ReviewCreateModel, session: AsyncSession):
        try:
            book = await book_service.get_book(book_uid, session)
            user = await user_service.get_user_by_email(user_email, session)

            new_review = Review(**review_data.model_dump(), user=user, book=book)

            if book is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                    )
            
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                    )

            session.add(new_review)
            await session.commit()
            return new_review
        except Exception as e:
            logging.exception(str(e))
            raise HTTPException(status_code=500, detail=f"An error occurred while adding the review: {str(e)}")


    async def get_all_user_reviews(self, user_uid: str, session: AsyncSession):
        statement = select(Review).where(Review.user_uid == user_uid).order_by(desc(Review.created_at))
        result = await session.exec(statement)
        reviews = result.all()
        return reviews


    async def get_all_reviews(self, session: AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))
        result = await session.exec(statement)
        reviews = result.all()
        return reviews


    async def get_review_by_uid(self, review_uid: str, session: AsyncSession):
        statement = select(Review).where(Review.uid == review_uid)
        result = await session.exec(statement)
        return result.first()


    async def delete_review(self, review_uid: str, user_email: str, session: AsyncSession):

        user = await user_service.get_user_by_email(user_email, session)

        review_to_delete = await self.get_review_by_uid(review_uid, session)
        
        if review_to_delete is None or review_to_delete.user != user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found or you do not have permission to delete this review"
            )
        
        await session.delete(review_to_delete)
        await session.commit()