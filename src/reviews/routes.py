from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User
from src.auth.dependencies import get_current_user, RoleChecker
from .service import ReviewService
from .schema import ReviewCreateModel
from src.db.main import get_session

review_router = APIRouter()
review_service = ReviewService()
user_role_check = Depends(RoleChecker(["user", "admin"]))
admin_role_check = Depends(RoleChecker(["admin"]))

@review_router.get("/", dependencies=[admin_role_check])
async def get_all_reviews(session: AsyncSession = Depends(get_session)):
    reviews = await review_service.get_all_reviews(session)
    return reviews

@review_router.get("/{review_uid}", dependencies=[user_role_check])
async def get_review(review_uid: str, session: AsyncSession = Depends(get_session)):
    review = await review_service.get_review_by_uid(review_uid, session)
    if review:
        return review
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

@review_router.post("/book/{book_uid}", status_code=status.HTTP_201_CREATED, dependencies=[user_role_check])
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


@review_router.delete("/{review_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[user_role_check])
async def delete_review(review_uid: str, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    await review_service.delete_review(review_uid, current_user.email, session)

    return None