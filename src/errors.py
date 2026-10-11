from typing import Any, Callable
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

class BooklyException(Exception):
    """Base class for all exceptions in the Bookly application."""
    pass

class InvalidTokenError(BooklyException):
    """User has provided an invalid or expired token."""
    pass

class RevokedToken(BooklyException):
    """User has provided a token that has been revoked."""
    pass

class AccessTokenRequired(BooklyException):
    """User has provided a refresh token instead of an access token."""
    pass

class RefreshTokenRequired(BooklyException):
    """User has provided an access token instead of a refresh token."""
    pass

class UserAlreadyExists(BooklyException):
    """User has provided an email that is already in use."""
    pass

class InvalidCredentials(BooklyException):
    """User has provided wrong email or password during signup."""
    pass

class InsufficientPermissions(BooklyException):
    """User does not have the required permissions to access a resource."""
    pass

class BookNotFound(BooklyException):
    """Book not found."""
    pass

class TagNotFound(BooklyException):
    """Tag not found."""
    pass

class TagAlreadyExist(BooklyException):
    """Tag already exists."""
    pass

class UserNotFound(BooklyException):
    """User not found."""
    pass

def create_exception_handler(status_code: int, initial_detail: Any) -> Callable[[Request, BooklyException], JSONResponse]:

    async def exception_handler(request: Request, exc: BooklyException) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={"detail": str(exc) or initial_detail},
        )

    return exception_handler

def register_exception_handlers(app: FastAPI) -> None:
        
        app.add_exception_handler(
            UserAlreadyExists,
            create_exception_handler(
                status_code=400,
                initial_detail={
                    "message": "User with this email already exists",
                    "error_code": "USER_ALREADY_EXISTS"
                    }
                )
        )
        app.add_exception_handler(
            BookNotFound,
            create_exception_handler(
                status_code=404,
                initial_detail={
                    "message": "Book not found",
                    "error_code": "BOOK_NOT_FOUND"
                }
            )
        )
        app.add_exception_handler(
            TagNotFound,
            create_exception_handler(
                status_code=404,
                initial_detail={
                    "message": "Tag not found",
                    "error_code": "TAG_NOT_FOUND"
                }
            )
        )
        app.add_exception_handler(
            TagAlreadyExist,
            create_exception_handler(
                status_code=400,
                initial_detail={
                    "message": "Tag already exists",
                    "error_code": "TAG_ALREADY_EXISTS"
                }
            )
        )
        app.add_exception_handler(
            UserNotFound,
            create_exception_handler(
                status_code=404,
                initial_detail={
                    "message": "User not found",
                    "error_code": "USER_NOT_FOUND"
                }
            )
        )
        app.add_exception_handler(
            AccessTokenRequired,
            create_exception_handler(
                status_code=400,
                initial_detail={
                    "message": " Provide a valid Access token",
                    "resolution": "Get an access token",
                    "error_code": "ACCESS_TOKEN_REQUIRED"
                }
            )
        )
        app.add_exception_handler(
            RefreshTokenRequired,
            create_exception_handler(
                status_code=400,
                initial_detail={
                    "message": " Provide a valid Refresh token",
                    "resolution": "Get a refresh token",
                    "error_code": "REFRESH_TOKEN_REQUIRED"
                }
            )
        )
        app.add_exception_handler(
            InvalidTokenError,
            create_exception_handler(
                status_code=401,
                initial_detail={
                    "message": "Invalid token",
                    "resolution": "Get a valid token",
                    "error_code": "INVALID_TOKEN"
                }
            )
        )
        app.add_exception_handler(
            RevokedToken,
            create_exception_handler(
                status_code=401,
                initial_detail={
                    "message": "Revoked token",
                    "resolution": "Get a new token",
                    "error_code": "REVOKED_TOKEN"
                }
            )
        )
        app.add_exception_handler(
            InsufficientPermissions,
            create_exception_handler(
                status_code=403,
                initial_detail={
                    "message": "You do not have the required permissions to access this resource",
                    "error_code": "INSUFFICIENT_PERMISSIONS"
                }
            )
        )
        app.add_exception_handler(
            InvalidCredentials,
            create_exception_handler(
                status_code=401,
                initial_detail={
                    "message": "Invalid Email or Password",
                    "error_code": "INVALID_EMAIL_OR_PASSWORD"
                }
            )
        )

        @app.exception_handler(500)
        async def internal_server_error_handler(request, exc):
            return JSONResponse(
                status_code=500,
                content={
                    "message": "Oops! An unexpected error occurred. Please try again later.",
                    "error_code": "INTERNAL_SERVER_ERROR"
                },
            )