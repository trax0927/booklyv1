from fastapi import APIRouter, status, Depends, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from .schemas import ( 
    UserCreateModel,
    UserModel, 
    UserLoginModel, 
    UserBooksModel, 
    EmailModel,
    PasswordResetModel,
    PasswordResetConfirmModel
     )
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.errors import InvalidCredentials, UserAlreadyExists, UserNotFound

from src.db.redis import add_token_to_blacklist
from .utils import (
    create_access_token,
    verify_password_hash,
    create_safe_url_token, 
    decode_safe_url_token,
    generate_password_hash
    )
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.config import Config
from src.celery_tasks import send_email

from datetime import timedelta


userService = UserService()
auth_router = APIRouter()
role_checker = RoleChecker(required_roles=["admin", "user"])

REFRESH_TOKEN_EXPIRE_MINUTES = 5

@auth_router.post("/send_email")
async def send_mail(emails:EmailModel):

    emails = emails.addresses

    html = "<h1>Welcome to Bookly</h1><p>Thank you for registering with us. We are excited to have you on board!</p>"
    subject = "Welcome to Bookly"

    send_email.delay(emails, subject, html)

    return {"message": "Email sent successfully"}

@auth_router.get('/verify_email/{token}')
async def verify_email(token: str, session: AsyncSession = Depends(get_session)):

    payload = decode_safe_url_token(token)
    email = payload.get('email') if payload else None

    if email:
        user = await userService.get_user_by_email(email, session)
        if not user:
            raise UserNotFound()

        await userService.update_user(user, {"is_verified": True}, session)
        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK
            )

    return JSONResponse(
        content={"message": "Error occured during verification"},
        status_code=status.HTTP_400_BAD_REQUEST
        )

@auth_router.post(
        '/register',
        status_code=status.HTTP_201_CREATED
        )
async def register_user(
    user_data: UserCreateModel,
    bg_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
    ):
    email = user_data.email

    user_exits = await userService.user_exists(email, session)
    if user_exits:
        raise UserAlreadyExists()

    new_user = await userService.create_user(user_data, session)

    token = create_safe_url_token({'email': email})

    html = f"""
    <h1>Verify your Email</h1>
    <p>Please click the link below to verify your email address:</p>
    <a href="https://{Config.DOMAIN_NAME}/api/v1/auth/verify_email/{token}">Verify Email</a>
    """
    emails = [email]
    subject = "Verify your Email"

    send_email.delay(emails, subject, html)

    return {
        "message": "User registered successfully. Please check your email to verify your account.",
        "user": new_user
    }

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

    raise InvalidCredentials()

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

@auth_router.get('/me', response_model=UserBooksModel)
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

@auth_router.post('/reset_password/{token}')
async def reset_password(token: str, password_data: PasswordResetConfirmModel, session: AsyncSession = Depends(get_session)):

    payload = decode_safe_url_token(token)
    email = payload.get('email') if payload else None

    if email:
        user = await userService.get_user_by_email(email, session)
        if not user:
            raise UserNotFound()

        new_password = password_data.new_password
        confirm_new_password = password_data.confirm_new_password

        if new_password != confirm_new_password:
            return JSONResponse(
                content={"message": "Passwords do not match"},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        passwd_hash = generate_password_hash(new_password)
        await userService.update_user(user, {"password_hash": passwd_hash}, session)
        return JSONResponse(
            content={"message": "Password reset successfully"},
            status_code=status.HTTP_200_OK
            )

    return JSONResponse(
        content={"message": "Error occured during password reset"},
        status_code=status.HTTP_400_BAD_REQUEST
        )

@auth_router.post('/reset_password_request')
async def reset_password_request(email_data: PasswordResetModel, session: AsyncSession = Depends(get_session)):

    email = email_data.email
    user = await userService.get_user_by_email(email, session)

    if not user:
        raise UserNotFound()

    token = create_safe_url_token({'email': email})

    html_message = f"""
    <h1>Reset your Password</h1>
    <p>Please click the link below to reset your password:</p>
    <a href="https://{Config.DOMAIN_NAME}/api/v1/auth/reset_password/{token}">Reset Password</a>
    """

    send_email.delay([email], "Reset your Password", html_message)

    return JSONResponse(
        content={"message": "Password reset email sent successfully"},
        status_code=status.HTTP_200_OK
    )