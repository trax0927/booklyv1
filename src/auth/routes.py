from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .utils import create_access_token, decode_access_token, verify_password_hash
from fastapi.responses import JSONResponse
from datetime import timedelta
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_token_to_blacklist

userService = UserService()
auth_router = APIRouter()
role_checker = RoleChecker(required_roles=["admin", "user"])

REFRESH_TOKEN_EXPIRE_MINUTES = 5

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

@auth_router.get('/refresh_token')
async def get_new_access_token(token_details: dict=Depends(RefreshTokenBearer())):
    new_access_token = create_access_token(
        user_data=token_details['user'],
        )
    return JSONResponse(
        content={
            "message": "New access token generated",
            "access_token": new_access_token
        }
    )

@auth_router.get('/me', response_model=UserModel)
async def get_me(user = Depends(get_current_user), _ : bool = Depends(role_checker)):
    return user

@auth_router.get('/logout')
async def logout_user(token_details: dict=Depends(AccessTokenBearer())):

    jti = token_details['jti']
    await add_token_to_blacklist(jti)
    return JSONResponse(
        content={
            "message": "Logout successful, token has been revoked"
        },
        status_code=status.HTTP_200_OK
    )