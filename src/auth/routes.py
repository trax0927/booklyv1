from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .utils import create_access_token, decode_access_token, verify_password_hash
from fastapi.responses import JSONResponse
from datetime import timedelta

userService = UserService()
auth_router = APIRouter()

REFRESH_TOKEN_EXPIRE_MINUTES = 3

@auth_router.post(
        '/register',
        response_model=UserModel,
        status_code=status.HTTP_201_CREATED
        )
async def register_user(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session)
    ):
    email = user_data.email

    user_exits = await userService.user_exists(email, session)
    if user_exits:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with email already exists")

    new_user = await userService.create_user(user_data, session)

    return new_user

@auth_router.post('/login')
async def login_user(user_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    user = await userService.get_user_by_email(user_data.email, session)
    if user is not None:
        user_verified = verify_password_hash(user_data.password, user.password_hash)

        if user_verified:
            user_data_dict = user.model_dump(mode="json", exclude={"password_hash"})
            access_token = create_access_token(user_data_dict)
            refresh_token = create_access_token(
                user_data_dict,
                timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
                refresh=True,
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
            