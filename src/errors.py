from typing import Any, Callable
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