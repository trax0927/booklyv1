from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User
from src.auth.dependencies import get_current_user
from .service import ReviewService
from .schema import ReviewCreateModel
from src.db.main import get_session

review_router = APIRouter()
review_service = ReviewService()

@review_router.post("/book/{book_uid}", status_code=status.HTTP_201_CREATED)
async def add_review(book_uid: str, review_data: ReviewCreateModel, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    try:
        new_review = await review_service.add_review(
            user_email=current_user.email,
            book_uid=book_uid,
            review_data=review_data,
            session=session
            )
        
        return new_review
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while adding the review: {str(e)}")